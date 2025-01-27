from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.db.wishes.crud import WishCRUD
from src.tgbot.my_wish_lists.members.states import MembersSG
from src.tgbot.my_wish_lists.states import MyWishListSG
from src.tgbot.my_wish_lists.wishes.dto.my_wish_list_dto import MyWishListsDTO
from src.tgbot.my_wish_lists.wishes.states import CreateWishSG, EditWishSG


async def go_to_members(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)

    await dialog_manager.start(MembersSG.list_of_members, data={'wish_list_id': dto.data.selected_wish_list_id})


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


async def go_to_create_wish(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)

    await dialog_manager.start(CreateWishSG.name, data={'wish_list_id': dto.data.selected_wish_list_id})


async def go_to_edit_name(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)
    await dialog_manager.start(EditWishSG.name, data={'wish_id': dto.data.selected_wish})


async def go_to_edit_photo(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)
    await dialog_manager.start(EditWishSG.photos, data={'wish_id': dto.data.selected_wish})


async def go_to_edit_description(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)
    await dialog_manager.start(EditWishSG.description, data={'wish_id': dto.data.selected_wish})


async def go_to_edit_link(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)
    await dialog_manager.start(EditWishSG.link_to_marketplace, data={'wish_id': dto.data.selected_wish})

async def go_to_edit_price(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)
    await dialog_manager.start(EditWishSG.price, data={'wish_id': dto.data.selected_wish})

