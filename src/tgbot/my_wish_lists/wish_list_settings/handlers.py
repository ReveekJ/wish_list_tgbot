from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner

from src.db.wish_lists.crud import WishListCRUD
from src.tgbot.my_wish_lists.wish_list_settings.dto.wish_list_settings_dto import WishListSettingsDTO
from src.tgbot.my_wish_lists.wish_list_settings.states import WishListSettingsSG


async def on_start_wish_list_settings(start_data: dict, dialog_manager: DialogManager, *args, **kwargs):
    if start_data.get('wish_list_id') is None:
        raise TypeError('start_data must contain "wish_list_id"')

    dto = WishListSettingsDTO(dialog_manager)
    dto.data.wish_list_id = start_data.get('wish_list_id')
    dto.save_to_dialog_manager(dialog_manager)


async def new_name_of_wish_list(message: Message, widget: MessageInput, dialog_manager: DialogManager, *args, **kwargs):
    dto = WishListSettingsDTO(dialog_manager)
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')

    with WishListCRUD() as crud:
        if crud.does_wish_list_exist_by_user_id_n_wish_list_name(message.from_user.id, message.text):
            await message.answer(i18n.get('same-name-of-wish-list-exists'))
            await dialog_manager.switch_to(WishListSettingsSG.new_name, show_mode=ShowMode.DELETE_AND_SEND)
            return

        crud.update(dto.data.wish_list_id, {'name': message.text})

    await message.answer(i18n.get('settings-wish-list-name-successfully-changed'))
    await dialog_manager.switch_to(WishListSettingsSG.select_action, show_mode=ShowMode.DELETE_AND_SEND)


async def delete_wish_list(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = WishListSettingsDTO(dialog_manager)

    with WishListCRUD() as crud:
        crud.delete(dto.data.wish_list_id)

    await dialog_manager.done(result={'is_deleted': True})


async def on_close_when_delete_wish_list(close_data: dict, dialog_manager: DialogManager, *args, **kwargs):
    if isinstance(close_data, dict):
        if close_data.get('is_deleted'):
            await dialog_manager.done()
