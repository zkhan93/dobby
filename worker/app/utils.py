import config
import redis

def get_redis():
    return redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, decode_responses=True)