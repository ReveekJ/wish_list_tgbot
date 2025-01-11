from aiogram.enums import ContentType
from aiogram.types import User as AiogramUser
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from src.db.wish_lists.crud import WishListCRUD
from src.db.wishes.crud import WishCRUD
from src.tgbot.my_wish_lists.create_wish_dto import CreateWishDTO
from src.tgbot.my_wish_lists.my_wish_list_dto import MyWishListsDTO


async def wish_lists_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    with WishListCRUD() as crud:
        wish_lists = crud.get_wish_lists_by_user_id(event_from_user.id)

    return {'wish_lists': [(i.id, i.name) for i in wish_lists]}


async def wishes_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = MyWishListsDTO(dialog_manager)

    with WishListCRUD() as crud:
        wish_list = crud.get_obj_by_id(dto.data.selected_wish_list_id)

    return {'wishes': [(i.id, i.name) for i in wish_list.wishes], 'wish_list_id': dto.data.selected_wish_list_id}


async def wish_preview_on_creation_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = CreateWishDTO(dialog_manager).data

    return {
        'name': dto.name,
        'photos': MediaAttachment(type=ContentType.PHOTO, path=dto.photos[0]) if dto.photos is not None else None,
        'link': dto.link_to_marketplace,
        'price': dto.price,
        'description': dto.description
    }


async def wish_preview_getter_on_edit_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = MyWishListsDTO(dialog_manager)

    with WishCRUD() as crud:
        wish = crud.get_obj_by_id(dto.data.selected_wish)

    return {
        'name': wish.name,
        'photos': MediaAttachment(type=ContentType.PHOTO, path=wish.photo) if wish.photo is not None else None,
        'link': wish.link_to_marketplace,
        'price': wish.price,
        'description': wish.description
    }
