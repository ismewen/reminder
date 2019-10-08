from redis import Redis
from django.conf import settings

redis_client = Redis.from_url(settings.REDIS_CON_URI)
