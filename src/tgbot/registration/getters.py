from aiogram.types import User
from aiogram_dialog import DialogManager

from src.db.users.enums import GenderEnum


async def gender_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    return {'genders': [(gender.name, gender.value) for gender in GenderEnum]}
