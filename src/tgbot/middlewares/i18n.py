from typing import Any, Dict, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import User, TelegramObject
from dishka import AsyncContainer
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get('event_from_user')

        if user is None:
            return await handler(event, data)

        dishka_container: AsyncContainer = data.get('dishka_container')
        hub = await dishka_container.get(TranslatorHub)
        data['i18n'] = hub.get_translator_by_locale(locale=user.language_code)

        return await handler(event, data)
