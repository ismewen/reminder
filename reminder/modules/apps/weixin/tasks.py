import arrow
from celery import group
from celery.utils.log import get_task_logger

from common.services.celery import celery
from common.services.redis import redis_client
from common.services.wechat import wechat_client
from modules.apps.weixin.models import BirthDayRecord


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
    start = now.shift(days=-45)
    records = BirthDayRecord.objects.filter(birth_day__gte=start.date()).filter(birth_day__lte=now.date()).all()
    birth_day_records = [record for record in records if
                         record.today_is_birth_day() and not redis_client.exists(record.has_reminder_key)]
    if birth_day_records:
        group(notice_user.s(i.id) for i in birth_day_records)()


@celery.task(bind=False)
def notice_user(id):
    obj = BirthDayRecord.objects.get(id=id)
    current_date = arrow.get(obj.birth_day).format('YYYY-MM-DD')
    way = "农历" if obj.is_lunar_calendar == 1 else "公历"
    text = "今天是{way}{current_date},{name}过生日,别忘了送上你的祝福".format(way=way, current_date=current_date, name=obj.name)
    wechat_client.message.send_text(obj.user.open_id, text)
    redis_client.set(obj.has_reminder_key, 1, 60 * 60 * 24)
