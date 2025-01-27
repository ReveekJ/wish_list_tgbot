from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel, SwitchTo, Button
from aiogram_dialog.widgets.text import Format

from src.custom_widgets.custom_back_button import BackButton
from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.my_wish_lists.getter import wish_lists_getter, wishes_getter, wish_preview_getter_on_edit_getter
from src.tgbot.my_wish_lists.handlers import wish_list_click_handler, wish_select_handler, go_to_create_wish, \
    go_to_edit_name, delete_wish, go_to_edit_link, go_to_edit_price, go_to_edit_description, go_to_edit_photo, \
    go_to_members
from src.tgbot.my_wish_lists.states import MyWishListSG
from src.tgbot.shared.wish_view import WishView

my_wish_lists_dialog = Dialog(
    Window(
        I18NFormat('select-wish-list'),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='my_wish_lists',
                item_id_getter=lambda item: item[0],
                items='wish_lists',
                on_click=wish_list_click_handler
            ),
            width=1,
            height=8,
            id='my_wish_lists_scrolling_group',
        ),
        Cancel(
            I18NFormat('back')
        ),
        getter=wish_lists_getter,
        state=MyWishListSG.list_of_wish_lists
    ),
    Window(
        I18NFormat('action-with-wish-list'),
        SwitchTo(
            I18NFormat('wishes-in-wish-list'),
            id='switch_to_wishes',
            state=MyWishListSG.list_of_wishes
        ),
        Button(
            I18NFormat('friends-in-wish-list'),
            id='switch_to_members',
            on_click=go_to_members
        ),
        BackButton(
            state=MyWishListSG.list_of_wish_lists,
        ),
        state=MyWishListSG.action_in_wish_list
    ),
    Window(
        I18NFormat('list-of-wishes'),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='wishes_select',
                item_id_getter=lambda item: item[0],
                items='wishes',
                on_click=wish_select_handler
            ),
            id='wishes_scrolling_group',
            width=1,
            height=8
        ),
        Button(
            I18NFormat('create-wish-button'),
            id='create_wish',
            on_click=go_to_create_wish
        ),
        BackButton(
            state=MyWishListSG.action_in_wish_list
        ),
        getter=wishes_getter,
        state=MyWishListSG.list_of_wishes
    ),
    WishView.preview_wish(
        Button(
            I18NFormat('edit-name'),
            id='edit_name',
            on_click=go_to_edit_name
        ),
        Button(
            I18NFormat('edit-photo'),
            id='edit_photo',
            on_click=go_to_edit_photo
        ),
        Button(
            I18NFormat('edit-description'),
            id='edit_description',
            on_click=go_to_edit_description
        ),
        Button(
            I18NFormat('edit-link-to-marketplace'),
            id='edit_link',
            on_click=go_to_edit_link
        ),
        Button(
            I18NFormat('edit-price'),
            id='edit_price',
            on_click=go_to_edit_price
        ),
        SwitchTo(
            I18NFormat('delete-wish'),
            id='switch_to_delete_wish',
            state=MyWishListSG.delete_wish
        ),
        BackButton(
            state=MyWishListSG.list_of_wishes,
        ),
        getter=wish_preview_getter_on_edit_getter,
        state=MyWishListSG.action_with_wish
    ),
    Window(
        I18NFormat('deleting-wish-approve'),
        Button(
            I18NFormat('delete-wish'),
            id='delete_btn',
            on_click=delete_wish
        ),
        SwitchTo(
            I18NFormat('no-delete'),
            id='no_delete',
            state=MyWishListSG.action_with_wish
        ),
        BackButton(
            state=MyWishListSG.action_with_wish
        ),
        state=MyWishListSG.delete_wish
    ),
)
