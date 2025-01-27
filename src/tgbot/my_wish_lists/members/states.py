from aiogram.fsm.state import StatesGroup, State


class MembersSG(StatesGroup):
    list_of_members  = State()
    add_member = State()
    action_with_member = State()
    approve_delete_member = State()
