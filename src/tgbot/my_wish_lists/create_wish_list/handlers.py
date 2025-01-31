from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from src.db.wish_lists.crud import WishListCRUD
from src.db.wish_lists.schemas import WishList
from src.tgbot.my_wish_lists.create_wish_list.dto.create_wish_list_dto import CreateWishListDTO
from src.tgbot.my_wish_lists.create_wish_list.states import CreateWishListSG


async def name_of_new_wish_list(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dto = CreateWishListDTO(dialog_manager)

    # проверяем есть ли уже такой wishlist
    with WishListCRUD() as crud:
        if crud.does_wish_list_exist_by_user_id_n_wish_list_name(message.from_user.id, message.text):
            await dialog_manager.switch_to(CreateWishListSG.name)
            return

        dto.data.name = message.text
        dto.save_to_dialog_manager(dialog_manager)

        wish_list = WishList(
            owner_id=message.from_user.id,
            name=dto.data.name,
        )
        crud.create(wish_list)

    await dialog_manager.done()
