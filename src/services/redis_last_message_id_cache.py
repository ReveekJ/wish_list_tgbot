from typing import Optional

from redis.asyncio import Redis

from src.config import REDIS_HOST, REDIS_PORT, CACHE_LAST_MESSAGE_ID


class RedisLastMessageIdCache:
    def __init__(self):
        self.__r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=CACHE_LAST_MESSAGE_ID)

    async def set(self, user_id: int, message_id: int) -> None:
        await self.__r.set(str(user_id), str(message_id))

    async def get(self, user_id: int) -> Optional[int]:
        return await self.__r.get(str(user_id))

    async def delete(self, user_id: int) -> None:
        await self.__r.delete(str(user_id))
