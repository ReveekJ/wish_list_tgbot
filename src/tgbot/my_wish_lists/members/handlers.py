from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner

from src.db.wish_list_members_secondary.crud import WishListMembersSecondaryCRUD
from src.tgbot.my_wish_lists.members.dto.members_list_dto import MembersListDTO
from src.tgbot.my_wish_lists.members.states import MembersSG


async def on_start_member_dialog(start_data: dict, dialog_manager: DialogManager, *args, **kwargs):
    if start_data.get('wish_list_id') is None:
        raise TypeError('start_data must contain "wish_list_id"')

    dto = MembersListDTO(dialog_manager)
    dto.data.wish_list_id = start_data['wish_list_id']
    dto.save_to_dialog_manager(dialog_manager)


async def select_member(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = MembersListDTO(dialog_manager)

    dto.data.selected_member = int(callback.data.split(':')[-1])
    dto.save_to_dialog_manager(dialog_manager)

    await dialog_manager.switch_to(MembersSG.action_with_member)


async def delete_member(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    dto = MembersListDTO(dialog_manager)

    with WishListMembersSecondaryCRUD() as crud:
        crud.delete_pair(dto.data.selected_member, dto.data.wish_list_id)

    await callback.message.answer(i18n.get('successfully-delete-member'))
    await dialog_manager.switch_to(MembersSG.list_of_members, show_mode=ShowMode.DELETE_AND_SEND)
