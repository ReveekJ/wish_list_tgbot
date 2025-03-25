from aiogram_dialog import DialogManager
from aiogram.types import User as AiogramUser

from src.db.wish_lists.crud import WishListCRUD
from src.tgbot.my_wish_lists.members.dto.members_list_dto import MembersListDTO
from src.tgbot.my_wish_lists.members.utils.link_generator import get_link_for_member_invite
from src.tgbot.utils.name_username_concatenate import name_username_concatenate


async def members_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = MembersListDTO(dialog_manager)

    with WishListCRUD() as crud:
        wish_list = crud.get_obj_by_id(dto.data.wish_list_id)

    return {'members': [(i.id, name_username_concatenate(i)) for i in wish_list.members]}


async def link_for_member_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = MembersListDTO(dialog_manager)

    return {'link': await get_link_for_member_invite(event_from_user.bot, event_from_user.id, dto.data.wish_list_id)}
