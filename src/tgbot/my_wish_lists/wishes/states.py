from aiogram.fsm.state import StatesGroup, State


class MyWishListSG(StatesGroup):
    list_of_wish_lists = State()
    action_in_wish_list = State()
    list_of_wishes = State()
    list_of_members = State()
    action_with_wish = State()
    delete_wish = State()


class CreateWishSG(StatesGroup):
    name = State()
    photos = State()
    description = State()
    link_to_marketplace = State()
    price = State()
    preview = State()


class EditWishSG(StatesGroup):
    name = State()
    photos = State()
    description = State()
    link_to_marketplace = State()
    price = State()
