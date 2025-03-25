from typing import Optional

import redis

from src.config import REDIS_HOST, REDIS_PORT, CACHE_LAST_MESSAGE_ID


class RedisLastMessageIdCache:
    def __init__(self):
        self.__r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=CACHE_LAST_MESSAGE_ID)

    def set(self, user_id: int, message_id: int):
        self.__r.set(str(user_id), str(message_id))

    def get(self, user_id: int) -> Optional[int]:
        return self.__r.get(str(user_id))

    def delete(self, user_id: int):
        self.__r.delete(str(user_id))
