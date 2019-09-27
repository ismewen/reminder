from django.conf import settings
from wechatpy import WeChatClient
from wechatpy.session.redisstorage import RedisStorage

from common.services.redis import redis_client

session_interface = RedisStorage(
    redis_client,
    prefix="wechatpy"
)

wechat_client = WeChatClient(
    settings.COMPONENT_APP_ID,
    settings.COMPONENT_APP_SECRET,
    session=session_interface
)
