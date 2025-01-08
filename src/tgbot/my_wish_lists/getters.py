from aiogram.types import User as AiogramUser
from aiogram_dialog import DialogManager

from src.db.wish_lists.crud import WishListCRUD


async def wish_lists_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    with WishListCRUD() as crud:
        wish_lists = crud.get_wish_lists_by_user_id(event_from_user.id)

    return {'wish_lists': [(i.id, i.name) for i in wish_lists]}
