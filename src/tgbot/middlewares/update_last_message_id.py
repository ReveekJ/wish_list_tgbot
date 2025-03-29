from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery
from dishka import AsyncContainer

from src.services.redis_last_message_id_cache import RedisLastMessageIdCache


class UpdateLastMessageIdMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        if isinstance(event, CallbackQuery):
            callback = CallbackQuery(**event.model_dump())
            di_container: AsyncContainer = data.get("di_container")
            r = await di_container.get(RedisLastMessageIdCache)

            await r.set(callback.from_user.id, callback.message.message_id)

        return await handler(event, data)
