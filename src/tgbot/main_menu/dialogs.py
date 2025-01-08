from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start

from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.main_menu.states import MainMenuSG
from src.tgbot.my_wish_lists.states import MyWishListSG

main_dialog = Dialog(
    Window(
        I18NFormat('main-menu-greeting'),
        Start(
            I18NFormat('my-wish-lists'),
            id='my_wish_lists',
            state=MyWishListSG.list_of_wish_lists
        ),
        # Start(
        #     I18NFormat('my-friends'),
        #     id='my_friends',
        #     state=
        # ),
        state=MainMenuSG.main_menu
    )
)
