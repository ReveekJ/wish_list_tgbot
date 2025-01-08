from aiogram.fsm.state import StatesGroup, State


class RegistrationSG(StatesGroup):
    birthdate = State()
    gender = State()
