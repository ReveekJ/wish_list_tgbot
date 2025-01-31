from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput

from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.my_wish_lists.create_wish_list.handlers import name_of_new_wish_list
from src.tgbot.my_wish_lists.create_wish_list.states import CreateWishListSG

create_wish_list_dialog = Dialog(
    Window(
        I18NFormat('enter-name-of-new-wish-list'),
        MessageInput(
            func=name_of_new_wish_list,
            content_types=ContentType.TEXT,
        ),
        state=CreateWishListSG.name
    )
)
