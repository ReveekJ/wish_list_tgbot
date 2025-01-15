from aiogram.fsm.state import StatesGroup, State


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
