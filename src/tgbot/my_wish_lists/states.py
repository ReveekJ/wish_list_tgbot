from aiogram.fsm.state import StatesGroup, State


class MyWishListSG(StatesGroup):
    list_of_wish_lists = State()
    action_in_wish_list = State()
    list_of_wishes = State()
    action_with_wish = State()
    delete_wish = State()
    wish_fulfilled = State()
