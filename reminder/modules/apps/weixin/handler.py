import json
import logging
import re
import requests
from rest_framework.exceptions import ValidationError

from django.conf import settings
from wechatpy.events import SubscribeEvent

from common.services.wechat import wechat_client
from modules.apps.oauth.models import User
from modules.apps.weixin.models import BirthDayRecord
from modules.apps.weixin.serializers import BirthDayRecordSerializer

Group = {
    "support": 100,
    "develop": 101,
}


class PoorHandler(object):
    """
    穷人版的handle,针对特定text回复
    """
    handlers = []

    def filter(self, *args):
        def wraps(func):
            self.add_handle(func, list(args))
            return func

        return wraps

    def add_handle(self, func, rules):
        if len(rules) > 1:
            for x in rules:
                self.add_handle(func, [x])
        content = rules[0]
        if isinstance(content, str):
            def _check_content(message):
                return message.content == content
        elif isinstance(content, type(re.compile("regex_test"))):
            def _check_content(message):
                return content.match(message.content)
        else:
            raise Exception("%s is invalid rule" % content)

        def wraps(message):
            _check_result = _check_content(message)
            if _check_result:
                if isinstance(_check_result, bool):
                    _check_result = None
                return func(message)

        self.handlers.append(wraps)

    def handle_message(self, message):
        for func in self.handlers:
            res = func(message)
            if res:
                return res


class EventHandler(object):
    handlers = dict()

    def register(self, event_type):
        def wraps(func):
            self.handlers[event_type] = func
            return func
        return wraps

    def handle_message(self, message):
        func = self.get_handle(message.event)
        if func:
            return func(message)

    def get_handle(self, event_type):
        return self.handlers.get(event_type)


event_handle = EventHandler()

handler = PoorHandler()

uri = settings.SERVER_URL

logger = logging.getLogger('django')


@handler.filter(re.compile("^nansang add"))
def nansang_add(message):
    mandatory_args = ["-n", "-b", "-g", "-l"]
    fields_list = ["name", "birth_day", "group_name", "is_lunar_calendar"]
    content = message.content.lstrip("nansang add").split(" ")
    error_message = "error format, nansang add -n name -b xxxx-xx-xx -g group -l"
    try:
        mapping = {fields_list[index]: content[content.index(x) + 1] for index, x in enumerate(mandatory_args) if
                   x != -1 and x != "-l"}
    except (IndexError, ValueError):
        return error_message
    if len(mapping.keys()) != len(mandatory_args) - 1:
        return error_message
    mapping['is_lunar_calendar'] = 1 if '-l' not in content else 2  # 默认为农历
    mapping['open_id'] = message.source
    s = BirthDayRecordSerializer(data=mapping)
    try:
        s.is_valid(raise_exception=True)
    except ValidationError as e:
        return "failed due to %s" % e.default_detail
    s.save()
    return "success,the item id is %s" % s.instance.id


@handler.filter(re.compile("^nansang list$"))
def nansang_list(message):
    open_id = message.source
    t = "{id} {name} {birth_day} {group_name} {is_lunar_calendar} \n"
    res = BirthDayRecord.objects.filter(open_id=open_id).all()
    hi = BirthDayRecordSerializer(res, many=True)
    response_text = str()
    for x in hi.data:
        response_text += t.format(**x)
    return response_text


@handler.filter(re.compile("^nansang delete \d.*"))
def handler_delete(message):
    record_id = int(message.content.strip(" ").split(" ")[-1])
    s = BirthDayRecord.objects.filter(open_id=message.source, id=record_id).first()
    if not s:
        return "not found"
    s.delete()
    return 'success'


@handler.filter(re.compile("^ns upsert"))
def ns(message):
    ns = message.content.strip(" ").split(" ")
    if len(ns) < 3 or ns[2] not in ["support", "develop"]:
        return "错误的格式，请参考ns upsert support|develop name"
    group_name = ns[2]
    user = User.objects.filter(open_id=message.source).first()
    group_id = Group.get(group_name)
    if user:
        if user.group_name != group_name:
            user.group_name = group_name
            wechat_client.group.move_user(user_id=message.source, group_id=group_id)
        user.group_id = group_id
    else:
        user_info = wechat_client.user.get(message.source)
        user = User(username=user_info.get("nickname"), group_id=Group.get(group_name), open_id=message.source)
        wechat_client.group.move_user(user_id=user.open_id, group_id=group_id)
    user.save()
    return "success"


@event_handle.register('subscribe')
def subscribe(message: SubscribeEvent):
    logger.info("start handle subscribe message %s " % str(message))
    user = User.objects.all().filter(open_id=message.source).first()
    if not user:
        user_info = wechat_client.user.get(message.source)
        user = User(username=user_info.get("nickname"), opend_id=message.source)
        user.save()
    else:
        user.status = "Active"
        user.save()


@event_handle.register('unsubscribe')
def unsubscribe(message: SubscribeEvent):
    logger.info("start handle unsubscribe message %s" % str(message))
    user = User.objects.all().filter(open_id=message.source).first()
    if user:
        user.status = "InActive"
        user.save()



