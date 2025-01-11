from typing import Callable

from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.utils import GetterVariant


class WishView:
    @staticmethod
    def preview_wish(*custom_buttons: Keyboard, getter: GetterVariant, state: State) -> Window:
        return Window(
            Format('{name}\n'),
            DynamicMedia(
                'photos',
                when='photos'
            ),
            Format(
                '{description}\n',
                when='description'
            ),
            Format(
                '{link}\n',
                when='link'
            ),
            Format(
                '{price}\n',
                when='price'
            ),
            *custom_buttons,
            getter=getter,
            state=state
        )
