from aiogram.fsm.state import StatesGroup, State


class WishListSettingsSG(StatesGroup):
    select_action = State()
    new_name = State()
    delete_wish_list = State()
