from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Select, Group, SwitchTo
from aiogram_dialog.widgets.text import Format

from src.custom_widgets.birthdate_asking_calendar import BirthdateAskingCalendar
from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.registration.getters import gender_getter
from src.tgbot.registration.handlers import birthdate_select_handler, gender_select_handler
from src.tgbot.registration.states import RegistrationSG

registration_dialog = Dialog(
    Window(
        I18NFormat('ask-birthdate'),
        BirthdateAskingCalendar(
            id='test',
            on_click=birthdate_select_handler
        ),
        state=RegistrationSG.birthdate
    ),
    Window(
        I18NFormat('ask-gender'),
        Group(
            Select(
                I18NFormat('{item[1]}'),
                id='gender_select',
                item_id_getter=lambda item: item[0],
                items='genders',
                on_click=gender_select_handler
            ),
            width=1
        ),
        SwitchTo(
            I18NFormat('back'),
            id='back_to_birthdate',
            state=RegistrationSG.birthdate
        ),
        getter=gender_getter,
        state=RegistrationSG.gender
    )
)
