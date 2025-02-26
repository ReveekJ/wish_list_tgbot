import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedCalendar

from src.db.users.crud import UserCRUD
from src.db.users.enums import GenderEnum
from src.db.users.schemas import User
from src.services.schedule_notifications_manager.tasks.tasks import BirthdateNotificationManager, BirthdateNotificationConfig
from src.tgbot.main_menu.states import MainMenuSG
from src.tgbot.registration.dialog_data_dto import RegistrationDTO
from src.tgbot.registration.states import RegistrationSG
from src.tgbot.utils.name_username_concatenate import name_username_concatenate


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
        new_user = crud.create(
            User(
                id=callback.from_user.id,
                username=callback.from_user.username,
                name=callback.from_user.full_name,
                birthdate=dto.data.selected_birthdate,
                gender=dto.data.gender,
                language_code=callback.from_user.language_code
            )
        )

    # ставим уведомления о дне рождения
    notification_manager = BirthdateNotificationManager()
    await notification_manager.schedule_notifications(
        BirthdateNotificationConfig(
            user_id=new_user.id,
            birthdate=new_user.birthdate,
            notification_time=datetime.time(hour=8, minute=0),
            i18n_text='your_friends_birthday_today',
            i18n_params={
                'username': name_username_concatenate(new_user)
            }
        )
    )
    await notification_manager.schedule_notifications(
        BirthdateNotificationConfig(
            user_id=new_user.id,
            birthdate=new_user.birthdate - datetime.timedelta(days=7),
            i18n_text='your_friends_birthday_1_week_before',
            i18n_params={
                'username': name_username_concatenate(new_user)
            }
        )
    )

    # TODO: автоматически создать первый виш лист
    await dialog_manager.done()
    await dialog_manager.start(MainMenuSG.main_menu)
