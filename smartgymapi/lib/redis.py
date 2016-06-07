import redis

from smartgymapi.lib.decorators import singleton


@singleton
class RedisSession(object):
    def __init__(self, host, port, db):
        self.session = redis.StrictRedis(host=host, port=port, db=db)


def write_to_cache(key, value):
    RedisSession().session.set(key, value)


def get_from_cache(key):
    return RedisSession().session.get(key)
