from aiogram.fsm.state import StatesGroup, State


class CreateWishListSG(StatesGroup):
    name = State()
