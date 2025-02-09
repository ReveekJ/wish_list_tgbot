from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import User as AiogramUser

from src.db.users.crud import UserCRUD
from src.db.users.schemas import User


class UpdateUserDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        aiogram_user: AiogramUser = data.get('event_from_user')

        with UserCRUD() as crud:
            current_user: User = crud.get_obj_by_id(aiogram_user.id)
            if not current_user:
                return await handler(event, data)

            new_user = current_user.model_copy()

            if aiogram_user.username != current_user.username:
                new_user.username = aiogram_user.username
            if aiogram_user.full_name != current_user.name:
                new_user.name = aiogram_user.full_name

            if new_user != current_user:
                crud.update(current_user.id, new_user.model_dump())

        return await handler(event, data)
