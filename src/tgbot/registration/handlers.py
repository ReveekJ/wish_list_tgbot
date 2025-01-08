import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedCalendar

from src.db.users.crud import UserCRUD
from src.db.users.enums import GenderEnum
from src.db.users.schemas import User
from src.tgbot.main_menu.states import MainMenuSG
from src.tgbot.registration.dialog_data_dto import RegistrationDTO
from src.tgbot.registration.states import RegistrationSG


async def birthdate_select_handler(callback: CallbackQuery, widget: ManagedCalendar, dialog_manager: DialogManager, selected_date: datetime.date, *args, **kwargs):
    dto = RegistrationDTO(dialog_manager)
    dto.data.selected_birthdate = selected_date
    dto.save_to_dialog_manager(dialog_manager)

    await dialog_manager.switch_to(RegistrationSG.gender)


async def gender_select_handler(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager, *args, **kwargs):
    dto = RegistrationDTO(dialog_manager)
    dto.data.gender = GenderEnum[callback.data.split(':')[-1]]
    dto.save_to_dialog_manager(dialog_manager)

    # сохранить инфу в бд
    with UserCRUD() as crud:
        user_first_name = callback.from_user.first_name if callback.from_user.first_name is not None else ''
        user_last_name = callback.from_user.last_name if callback.from_user.last_name is not None else ''

        crud.create(
            User(
                id=callback.from_user.id,
                username=callback.from_user.username,
                name=f'{user_first_name} {user_last_name}',
                birthdate=dto.data.selected_birthdate,
                gender=dto.data.gender,
            )
        )

    # TODO: автоматически создать первый виш лист
    await dialog_manager.done()
    await dialog_manager.start(MainMenuSG.main_menu)
