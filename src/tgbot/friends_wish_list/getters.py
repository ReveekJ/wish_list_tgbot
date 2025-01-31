from aiogram.enums import ContentType
from aiogram.types import User as AiogramUser
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from src.db.users.crud import UserCRUD
from src.db.wish_lists.crud import WishListCRUD
from src.db.wishes.crud import WishCRUD
from src.tgbot.friends_wish_list.dto.friends_wish_list_dto import FriendsWishListDTO
from src.tgbot.utils.name_username_concatenate import name_username_concatenate


async def get_friends(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    with UserCRUD() as user_crud:
        friends = user_crud.get_friends_of_user(event_from_user.id)

    return {'friends': [(i.id, name_username_concatenate(i)) for i in friends]}


async def get_wish_list(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = FriendsWishListDTO(dialog_manager)

    with WishListCRUD() as wish_list_crud:
        wish_lists = wish_list_crud.get_wish_lists_by_user_id(dto.data.selected_friend_id)

    return {'wish_list': [(i.id, i.name) for i in wish_lists]}


async def get_wishes(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = FriendsWishListDTO(dialog_manager)

    with WishListCRUD() as wish_list_crud:
        wish_list = wish_list_crud.get_obj_by_id(dto.data.selected_wishlist_id)

    return {'wishes': [(i.id, i.name) for i in wish_list.wishes]}


async def get_wish_view(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = FriendsWishListDTO(dialog_manager)

    with WishCRUD() as wish_crud:
        wish = wish_crud.get_obj_by_id(dto.data.selected_wish_id)

    return {
        'name': wish.name,
        'photos': MediaAttachment(type=ContentType.PHOTO, path=wish.photo) if wish.photo is not None else None,
        'link': wish.link_to_marketplace,
        'price': wish.price,
        'description': wish.description,
        'show_reserve_btn': not wish.is_booked,
        'show_cancel_reserve_btn': True if wish.is_booked and wish.booked_by_user_id == event_from_user.id else False,
        'booked_true': wish.is_booked if wish.is_booked else None
    }
