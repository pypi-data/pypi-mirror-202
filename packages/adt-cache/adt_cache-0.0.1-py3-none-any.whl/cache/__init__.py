from abc import abstractmethod, ABCMeta
from typing import List
import redis


class AdtCache(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def intersect(self, key: str, vals: List):
        pass

    @abstractmethod
    def differential(self, key: str, vals: List):
        pass

    @abstractmethod
    def push_values(self, key: str, vals: List):
        pass


class RedisCache(AdtCache):
    def __init__(self, host: str, port, db):
        super().__init__()
        self.redis = redis.Redis(host=host, port=port, db=db)

    def intersect(self, key, vals: List):
        return [val for val in vals if self.redis.sismember(key, val)]

    def differential(self, key, vals: List):
        return [val for val in vals if not self.redis.sismember(key, val)]

    def push_values(self, key, vals: List):
        return self.redis.sadd(key, *set(vals))


class MemoryCache(AdtCache):
    def __init__(self):
        super().__init__()
        self.cache = {}

    def intersect(self, key, vals: List):
        return [val for val in vals if val in self.cache.get(key, [])]

    def differential(self, key, vals: List):
        return [val for val in vals if val not in self.cache.get(key, [])]

    def push_values(self, key, vals: List):
        c = self.cache.get(key)
        if c is None:
            self.cache[key] = set(vals)
        else:
            c.extend(set(vals))