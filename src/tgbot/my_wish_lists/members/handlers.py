from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

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
    