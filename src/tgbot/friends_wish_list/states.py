from aiogram.fsm.state import StatesGroup, State


class FriendsWishListSG(StatesGroup):
    friends_list = State()
    wish_list = State()
    wish = State()
    wish_view = State()

    reserve_wish = State()
    cancel_reserve_wish = State()
