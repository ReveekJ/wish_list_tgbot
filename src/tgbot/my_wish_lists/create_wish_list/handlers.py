from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from fluentogram import TranslatorRunner

from src.db.wish_lists.crud import WishListCRUD
from src.db.wish_lists.schemas import WishList
from src.tgbot.my_wish_lists.create_wish_list.dto.create_wish_list_dto import CreateWishListDTO
from src.tgbot.my_wish_lists.create_wish_list.states import CreateWishListSG


async def name_of_new_wish_list(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishListDTO(dialog_manager)
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')

    # проверяем есть ли уже такой wishlist
    with WishListCRUD() as crud:
        if crud.does_wish_list_exist_by_user_id_n_wish_list_name(message.from_user.id, message.text):
            await message.answer(i18n.get('same-name-of-wish-list-exists'))
            await dialog_manager.switch_to(CreateWishListSG.name, show_mode=ShowMode.DELETE_AND_SEND)
            return

        dto.data.name = message.text
        dto.save_to_dialog_manager(dialog_manager)

        wish_list = WishList(
            owner_id=message.from_user.id,
            name=dto.data.name,
        )
        crud.create(wish_list)

    await dialog_manager.done()
