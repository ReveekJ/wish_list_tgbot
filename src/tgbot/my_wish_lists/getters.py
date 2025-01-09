from aiogram.types import User as AiogramUser
from aiogram_dialog import DialogManager

from src.db.wish_lists.crud import WishListCRUD
from src.tgbot.my_wish_lists.dialog_data_dto import MyWishListsDTO


async def wish_lists_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    with WishListCRUD() as crud:
        wish_lists = crud.get_wish_lists_by_user_id(event_from_user.id)

    return {'wish_lists': [(i.id, i.name) for i in wish_lists]}


async def wishes_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = MyWishListsDTO(dialog_manager)

    with WishListCRUD() as crud:
        wish_list = crud.get_obj_by_id(dto.data.selected_wish_list_id)

    return {'wishes': [(i.id, i.name) for i in wish_list.wishes]}
