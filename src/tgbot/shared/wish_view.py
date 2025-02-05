from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Keyboard
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Multi
from aiogram_dialog.widgets.utils import GetterVariant

from src.custom_widgets.i18n_format import I18NFormat


class WishView:
    @staticmethod
    def preview_wish(*custom_buttons: Keyboard, getter: GetterVariant, state: State) -> Window:
        return Window(
            I18NFormat(
                'wish-is-booked',
                when='booked_true'
            ),
            Format('\n{name}\n'),
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
            Multi(
                I18NFormat(
                    'wish-cost',
                    when='price'
                ),
                Format(
                    '{price}\n',
                    when='price'
                ),
            ),
            *custom_buttons,
            getter=getter,
            state=state
        )
