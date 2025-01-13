from typing import Union, Optional

from aiogram.enums import ContentType
from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput, MessageHandlerFunc
from aiogram_dialog.widgets.kbd import Keyboard, SwitchTo, Back, Next
from aiogram_dialog.widgets.utils import GetterVariant
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor

from src.custom_widgets.i18n_format import I18NFormat


class WishEdit:
    @staticmethod
    def name_window(
            *custom_buttons: Keyboard,
            handler: Union[MessageHandlerFunc, WidgetEventProcessor, None],
            getter: Optional[GetterVariant] = None,
            state: State
    ) -> Window:
        return Window(
            I18NFormat('enter-name'),
            MessageInput(
                content_types=ContentType.TEXT,
                func=handler
            ),
            *custom_buttons,
            getter=getter,
            state=state
        )

    @staticmethod
    def photo_window(
            *custom_buttons: Keyboard,
            handler: Union[MessageHandlerFunc, WidgetEventProcessor, None],
            getter: Optional[GetterVariant] = None,
            state: State
    ) -> Window:
        return Window(
            I18NFormat('send-photos'),
            MessageInput(
                content_types=ContentType.PHOTO,
                func=handler
            ),
            Next(
                I18NFormat('skip-step'),
            ),
            Back(
                I18NFormat('back')
            ),
            getter=getter,
            state=state
        )

    @staticmethod
    def description_window(
            *custom_buttons: Keyboard,
            handler: Union[MessageHandlerFunc, WidgetEventProcessor, None],
            getter: Optional[GetterVariant] = None,
            state: State
    ) -> Window:
        return Window(
            I18NFormat('add-description'),
            MessageInput(
                content_types=ContentType.TEXT,
                func=handler
            ),
            Next(
                I18NFormat('skip-step'),
            ),
            Back(
                I18NFormat('back')
            ),
            *custom_buttons,
            getter=getter,
            state=state
        )

    @staticmethod
    def link_window(
            *custom_buttons: Keyboard,
            handler: Union[MessageHandlerFunc, WidgetEventProcessor, None],
            getter: Optional[GetterVariant] = None,
            state: State
    ) -> Window:
        return Window(
            I18NFormat('add-link-to-marketplace'),
            MessageInput(
                content_types=ContentType.TEXT,
                func=handler
            ),
            Next(
                I18NFormat('skip-step'),
            ),
            Back(
                I18NFormat('back')
            ),
            *custom_buttons,
            getter=getter,
            state=state
        )

    @staticmethod
    def price_window(
            *custom_buttons: Keyboard,
            handler: Union[MessageHandlerFunc, WidgetEventProcessor, None],
            getter: Optional[GetterVariant] = None,
            state: State
    ) -> Window:
        return Window(
            I18NFormat('add-price'),
            MessageInput(
                content_types=ContentType.TEXT,
                func=handler
            ),
            Next(
                I18NFormat('skip-step'),
            ),
            Back(
                I18NFormat('back')
            ),
            *custom_buttons,
            getter=getter,
            state=state
        )
