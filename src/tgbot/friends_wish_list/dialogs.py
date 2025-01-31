from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel, SwitchTo, Button
from aiogram_dialog.widgets.text import Format

from src.custom_widgets.custom_back_button import BackButton
from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.friends_wish_list.getters import get_friends, get_wish_list, get_wishes, get_wish_view
from src.tgbot.friends_wish_list.handlers import select_friend, select_wish, select_wish_list, reserve_wish, \
    cancel_reservation_wish
from src.tgbot.friends_wish_list.states import FriendsWishListSG
from src.tgbot.shared.wish_view import WishView

friends_wish_list_dialog = Dialog(
    Window(
        I18NFormat('select-friend'),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='friends_select',
                item_id_getter=lambda x: x[0],
                items='friends',
                on_click=select_friend
            ),
            id='friends_scrolling_group',
            width=2,
            height=8
        ),
        Cancel(
            I18NFormat('back'),
        ),
        getter=get_friends,
        state=FriendsWishListSG.friends_list
    ),
    Window(
        I18NFormat('friends-select-wish-list'),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='wish_list_select',
                item_id_getter=lambda x: x[0],
                items='wish_list',
                on_click=select_wish_list
            ),
            id='wish_list_scrolling_group',
            width=1,
            height=8
        ),
        BackButton(
            state=FriendsWishListSG.friends_list,
        ),
        getter=get_wish_list,
        state=FriendsWishListSG.wish_list,
    ),
    Window(
        I18NFormat('select-wish'),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='wish_select',
                item_id_getter=lambda x: x[0],
                items='wishes',
                on_click=select_wish
            ),
            id='wish_scrolling_group',
            width=2,
            height=8
        ),
        BackButton(
            state=FriendsWishListSG.wish_list,
        ),
        getter=get_wishes,
        state=FriendsWishListSG.wish
    ),
    WishView.preview_wish(
        SwitchTo(
            I18NFormat('reserve-wish'),
            id='reserve_wish',
            state=FriendsWishListSG.reserve_wish,
            when='show_reserve_btn'
        ),
        SwitchTo(
            I18NFormat('cancel-reservation'),
            id='cancel_reservation',
            state=FriendsWishListSG.cancel_reserve_wish,
            when='show_cancel_reserve_btn'
        ),
        BackButton(
            state=FriendsWishListSG.wish,
        ),
        getter=get_wish_view,
        state=FriendsWishListSG.wish_view,
    ),
    Window(
        I18NFormat('about-booking-wish'),
        Button(
            I18NFormat('reserve-wish'),
            id='reserve_wish',
            on_click=reserve_wish
        ),
        BackButton(
            state=FriendsWishListSG.wish_view
        ),
        state=FriendsWishListSG.reserve_wish
    ),
    Window(
        I18NFormat('about-cancel-reserve-wish'),
        Button(
            I18NFormat('cancel-reservation'),
            id='cancel_reservation',
            on_click=cancel_reservation_wish
        ),
        BackButton(
            state=FriendsWishListSG.wish_view
        ),
        state=FriendsWishListSG.cancel_reserve_wish
    ),
)
