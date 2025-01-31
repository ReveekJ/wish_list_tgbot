from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.db.wishes.crud import WishCRUD
from src.tgbot.friends_wish_list.dto.friends_wish_list_dto import FriendsWishListDTO
from src.tgbot.friends_wish_list.states import FriendsWishListSG


async def select_friend(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = FriendsWishListDTO(dialog_manager)

    dto.data.selected_friend_id = int(callback.data.split(':')[-1])
    dto.save_to_dialog_manager(dialog_manager)

    await dialog_manager.switch_to(FriendsWishListSG.wish_list)


async def select_wish_list(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = FriendsWishListDTO(dialog_manager)

    dto.data.selected_wishlist_id = int(callback.data.split(':')[-1])
    dto.save_to_dialog_manager(dialog_manager)

    await dialog_manager.switch_to(FriendsWishListSG.wish)


async def select_wish(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = FriendsWishListDTO(dialog_manager)

    dto.data.selected_wish_id = int(callback.data.split(':')[-1])
    dto.save_to_dialog_manager(dialog_manager)

    await dialog_manager.switch_to(FriendsWishListSG.wish_view)


async def reserve_wish(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = FriendsWishListDTO(dialog_manager)

    with WishCRUD() as crud:
        crud.update(dto.data.selected_wish_id, {'is_booked': True, 'booked_by_user_id': callback.from_user.id})

    await dialog_manager.switch_to(FriendsWishListSG.wish_view)


async def cancel_reservation_wish(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = FriendsWishListDTO(dialog_manager)

    with WishCRUD() as crud:
        crud.update(dto.data.selected_wish_id, {'is_booked': False, 'booked_by_user_id': None})

    await dialog_manager.switch_to(FriendsWishListSG.wish_view)
