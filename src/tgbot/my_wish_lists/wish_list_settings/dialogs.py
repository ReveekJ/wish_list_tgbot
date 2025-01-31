from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel, Button

from src.custom_widgets.custom_back_button import BackButton
from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.my_wish_lists.wish_list_settings.handlers import new_name_of_wish_list, on_start_wish_list_settings, \
    delete_wish_list, on_close_when_delete_wish_list
from src.tgbot.my_wish_lists.wish_list_settings.states import WishListSettingsSG

wish_list_settings_dialog = Dialog(
    Window(
        I18NFormat('settings-select-action'),
        SwitchTo(
            I18NFormat('settings-edit-name'),
            id='switch_to_edit_name',
            state=WishListSettingsSG.new_name
        ),
        SwitchTo(
            I18NFormat('settings-delete-wish-list'),
            id='switch_to_delete_wish_list',
            state=WishListSettingsSG.delete_wish_list
        ),
        Cancel(
            I18NFormat('back')
        ),
        state=WishListSettingsSG.select_action
    ),
    Window(
        I18NFormat('settings-enter-new-name-wish-list'),
        MessageInput(
            func=new_name_of_wish_list,
            content_types=ContentType.TEXT,
        ),
        BackButton(
            state=WishListSettingsSG.select_action,
        ),
        state=WishListSettingsSG.new_name
    ),
    Window(
        I18NFormat('settings-are-you-sure-delete-wish-list'),
        SwitchTo(
            I18NFormat('settings-no-delete-wish-list'),
            id='no_delete',
            state=WishListSettingsSG.select_action
        ),
        Button(
            I18NFormat('settings-delete-wish-list'),
            id='delete_wish_list',
            on_click=delete_wish_list
        ),
        BackButton(
            state=WishListSettingsSG.select_action,
        ),
        state=WishListSettingsSG.delete_wish_list,
    ),
    on_start=on_start_wish_list_settings,
    on_close=on_close_when_delete_wish_list
)