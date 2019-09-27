from redis import Redis

redis_client = Redis.from_url('redis://redis:6379/0')
