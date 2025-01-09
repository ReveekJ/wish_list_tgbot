from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.db.wishes.crud import WishCRUD
from src.tgbot.my_wish_lists.dialog_data_dto import MyWishListsDTO
from src.tgbot.my_wish_lists.states import MyWishListSG


async def wish_list_click_handler(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)
    dto.data.selected_wish_list_id = int(callback.data.split(':')[-1])
    dto.save_to_dialog_manager(dialog_manager)

    await dialog_manager.switch_to(MyWishListSG.action_in_wish_list)


async def wish_select_handler(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)
    dto.data.selected_wish = int(callback.data.split(':')[-1])
    dto.save_to_dialog_manager(dialog_manager)

    await dialog_manager.switch_to(MyWishListSG.action_with_wish)


async def delete_wish(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)

    with WishCRUD() as crud:
        crud.delete(dto.data.selected_wish)

    await dialog_manager.switch_to(MyWishListSG.list_of_wishes)
