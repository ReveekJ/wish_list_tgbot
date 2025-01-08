from typing import Optional

from aiogram.fsm.state import State
from aiogram_dialog import ShowMode
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.kbd.button import OnClick

from src.custom_widgets.i18n_format import I18NFormat


class BackButton(SwitchTo):
    def __init__(
            self,
            state: State,
            on_click: Optional[OnClick] = None,
            when: WhenCondition = None,
            show_mode: Optional[ShowMode] = None):
        super().__init__(
            text=I18NFormat('back'),
            id='__back__',
            state=state
        )
