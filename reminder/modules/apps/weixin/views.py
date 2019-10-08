import logging

from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from rachel.routers import router
from common.core.viewsets import APIView as CustomAPIView
from modules.apps.weixin.handler import handler
from modules.apps.weixin.models import BirthDayRecord
from modules.apps.weixin.serializers import BirthDayRecordSerializer

logger = logging.getLogger('django')


class WeiXinHandleView(APIView):
    def get(self, request, *args, **kwargs):
        logger.info("hello world %s %s %s" % (args, kwargs, request))
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(settings.COMPONENT_APP_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        response = HttpResponse(echo_str, content_type="text/plain")
        return response

    def post(self, request, *args, **kwargs):
        msg = parse_message(request.body)
        logger.info("hello world %s %s %s" % (args, kwargs, request))
        logger.info("hello msg %s %s" % (msg.type, msg))
        res = 'this is a %s message %s ' % (msg.type, msg)
        if msg.type == "text":
            res = handler.handle_message(msg)
        reply = create_reply(res, msg)
        logger.info("reply message %s " % res)
        response = HttpResponse(reply.render(), content_type="application/xml")
        return response


class WeiXinAPIView(CustomAPIView):
    custom_name = "birthday"
    path = 'birthday'
    model = BirthDayRecord
    serializer_class = BirthDayRecordSerializer
    allow_actions = 'create', 'update', 'list'
    filter_fields = ('open_id', 'name')


router.custom_register(WeiXinAPIView)
