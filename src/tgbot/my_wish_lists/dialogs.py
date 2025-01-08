from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel
from aiogram_dialog.widgets.text import Format

from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.my_wish_lists.getters import wish_lists_getter
from src.tgbot.my_wish_lists.states import MyWishListSG

my_wish_lists_dialog = Dialog(
    Window(
        I18NFormat('select-wish-list'),
        ScrollingGroup(
            Select(
                Format('{item[1}'),
                id='my_wish_lists',
                item_id_getter=lambda item: item[0],
                items='wish_lists'
            ),
            width=1,
            height=8,
            id='my_wish_lists_scrolling_group',
        ),
        Cancel(
            I18NFormat('back')
        ),
        getter=wish_lists_getter,
        state=MyWishListSG.list_of_wish_lists
    )
)