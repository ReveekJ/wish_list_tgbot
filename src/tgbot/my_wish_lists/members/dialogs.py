from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, SwitchTo, Cancel
from aiogram_dialog.widgets.text import Format

from src.custom_widgets.custom_back_button import BackButton
from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.my_wish_lists.members.getters import members_getter, link_for_member_getter
from src.tgbot.my_wish_lists.members.handlers import on_start_member_dialog, select_member
from src.tgbot.my_wish_lists.members.states import MembersSG


members_list_dialog = Dialog(
    Window(
        I18NFormat('select-member-of-wish-list'),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='members_select',
                item_id_getter=lambda item: item[0],
                items='members',
                on_click=select_member
            ),
            id='members_scrolling_group',
            width=1,
            height=8
        ),
        SwitchTo(
            I18NFormat('add-member'),
            id='add_member',
            state=MembersSG.add_member,
        ),
        Cancel(
            I18NFormat('back')
        ),
        state=MembersSG.list_of_members,
        getter=members_getter
    ),
    Window(
        I18NFormat('send-this-link-to-your-friend'),
        Format('\n{link}'),
        BackButton(
            state=MembersSG.list_of_members
        ),
        getter=link_for_member_getter,
        state=MembersSG.add_member
    ),
    Window(
        I18NFormat('choose-action-with-member'),
        SwitchTo(
            I18NFormat('delete-member'),
            id='delete_member',
            state=MembersSG.approve_delete_member
        ),
        BackButton(
            state=MembersSG.list_of_members
        ),
        state=MembersSG.action_with_member
    ),
    on_start=on_start_member_dialog
)
