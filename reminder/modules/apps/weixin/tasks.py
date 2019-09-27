import arrow
from celery import group
from celery.utils.log import get_task_logger

from services import celery
from services.wechat import wechat_client
from weixin.models import BirthDayRecord


@celery.task()
def test():
    print("this is a test")


@celery.task(bind=True)
def refresh_wechat_token(self):
    """
    刷新已授权公众号
    """
    logger = get_task_logger('refresh_wechat_token')

    try:
        result = wechat_client.fetch_access_token()
        logger.info(result)
    except Exception as e:
        logger.error(u'刷新已授权access token失败')


@celery.task(bind=True)
def find_the_star(self):
    """
    通知用户
    :param self:
    :return:
    """
    now = arrow.now()
    start = now.shift(days=-60)
    records = BirthDayRecord.objects.filter(birth_day__gte=start.date()).filter(birth_day__lte=now.date()).all()
    birth_day_records = [record for record in records if record.today_is_birth_day()]
    group(notice_user.s(i.id) for i in birth_day_records)()


@celery.task(bind=True)
def notice_user(id):
    obj = BirthDayRecord.objects.get(id=id)
    wechat_client.message.send_text(obj.open_id, "today is {name}'s birth day".format(name=obj.name))
