from aiogram import Bot
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.config import PATH_TO_WISH_IMAGES
from src.db.wishes.crud import WishCRUD
from src.db.wishes.schemas import Wish
from src.tgbot.my_wish_lists.create_wish_dto import CreateWishDTO
from src.tgbot.my_wish_lists.my_wish_list_dto import MyWishListsDTO
from src.tgbot.my_wish_lists.states import MyWishListSG, CreateWishSG
from src.utils.abstract_dialog_data_dto import DialogDataDTO


async def go_to_state_if_edit_mode(dto: DialogDataDTO, state_if_not_edit_mode: State, state_if_edit_mode: State, dialog_manager: DialogManager):
    if dto.data.edit_mode:
        await dialog_manager.switch_to(state_if_edit_mode)
    else:
        await dialog_manager.switch_to(state_if_not_edit_mode)


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


async def save_name(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishDTO(dialog_manager)
    dto.data.name = message.text
    dto.save_to_dialog_manager(dialog_manager)

    await go_to_state_if_edit_mode(dto, CreateWishSG.photos, CreateWishSG.preview, dialog_manager)


async def save_photos(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishDTO(dialog_manager)

    # сохраняем фото
    file_id = message.photo[-1].file_id
    path = PATH_TO_WISH_IMAGES + file_id + '.png'
    await message.bot.download(file_id, destination=path)

    dto.data.photos = [path]  # на самом деле список здесь не обязателен, но я его оставил, чтобы возможно в будущем сделать альбомы
    dto.save_to_dialog_manager(dialog_manager)

    # TODO: научить его принимать альбомы фото
    await go_to_state_if_edit_mode(dto, CreateWishSG.description, CreateWishSG.preview, dialog_manager)


async def save_description(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishDTO(dialog_manager)
    dto.data.description = message.text
    dto.save_to_dialog_manager(dialog_manager)

    await go_to_state_if_edit_mode(dto, CreateWishSG.link_to_marketplace, CreateWishSG.preview, dialog_manager)


async def save_link_to_marketplace(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishDTO(dialog_manager)
    dto.data.link_to_marketplace = message.text
    dto.save_to_dialog_manager(dialog_manager)

    await go_to_state_if_edit_mode(dto, CreateWishSG.price, CreateWishSG.preview, dialog_manager)


async def save_price(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishDTO(dialog_manager)
    dto.data.price = message.text
    dto.save_to_dialog_manager(dialog_manager)

    await dialog_manager.switch_to(CreateWishSG.preview)


async def create_wish_handler(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishDTO(dialog_manager).data

    with WishCRUD() as crud:
        wish = Wish(
            wish_list_id=dto.wish_list_id,
            name=dto.name,
            description=dto.description,
            link_to_marketplace=dto.link_to_marketplace,
            price=dto.price,
            photo=dto.photos[0] if dto.photos else None,
        )
        crud.create(wish)

    await dialog_manager.done()


async def on_start_create_wish_dialog(start_data: dict, dialog_manager: DialogManager, *args, **kwargs):
    if start_data.get('wish_list_id') is None:
        raise ValueError('On start dialog you should specify wish_list_id in start_data')

    dto = CreateWishDTO(dialog_manager)
    dto.data.wish_list_id = start_data.get('wish_list_id')
    dto.save_to_dialog_manager(dialog_manager)


async def go_to_create_wish(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MyWishListsDTO(dialog_manager)

    await dialog_manager.start(CreateWishSG.name, data={'wish_list_id': dto.data.selected_wish_list_id})


async def set_edit_mode(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishDTO(dialog_manager)
    dto.data.edit_mode = True
    dto.save_to_dialog_manager(dialog_manager)
