from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Cancel, SwitchTo, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format

from src.custom_widgets.custom_back_button import BackButton
from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.my_wish_lists.getters import wish_lists_getter, wishes_getter, wish_preview_on_creation_getter, \
    wish_preview_getter_on_edit_getter
from src.tgbot.my_wish_lists.handlers import wish_list_click_handler, wish_select_handler, delete_wish, \
    save_name, save_photos, save_description, save_link_to_marketplace, save_price, on_start_create_wish_dialog, \
    create_wish_handler, go_to_create_wish
from src.tgbot.my_wish_lists.states import MyWishListSG, CreateWishSG
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
        SwitchTo(
            I18NFormat('friends-in-wish-list'),
            id='switch_to_members',
            state=MyWishListSG.list_of_members
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

create_wish_dialog = Dialog(
    Window(
        I18NFormat('enter-name'),
        MessageInput(
            content_types=ContentType.TEXT,
            func=save_name
        ),
        state=CreateWishSG.name
    ),
    Window(
        I18NFormat('send-photos'),
        MessageInput(
            content_types=ContentType.PHOTO,
            func=save_photos
        ),
        SwitchTo(
            I18NFormat('skip-step'),
            id='skip_photo',
            state=CreateWishSG.description
        ),
        BackButton(
            state=CreateWishSG.name
        ),
        state=CreateWishSG.photos
    ),
    Window(
        I18NFormat('add-description'),
        MessageInput(
            content_types=ContentType.TEXT,
            func=save_description
        ),
        SwitchTo(
            I18NFormat('skip-step'),
            id='skip_description',
            state=CreateWishSG.link_to_marketplace
        ),
        BackButton(
            state=CreateWishSG.photos
        ),
        state=CreateWishSG.description
    ),
    Window(
        I18NFormat('add-link-to-marketplace'),
        MessageInput(
            content_types=ContentType.TEXT,
            func=save_link_to_marketplace
        ),
        SwitchTo(
            I18NFormat('skip-step'),
            id='skip_link',
            state=CreateWishSG.price
        ),
        BackButton(
            state=CreateWishSG.description
        ),
        state=CreateWishSG.link_to_marketplace
    ),
    Window(
        I18NFormat('add-price'),
        MessageInput(
            content_types=ContentType.TEXT,
            func=save_price
        ),
        SwitchTo(
            I18NFormat('skip-step'),
            id='skip_price',
            state=CreateWishSG.preview
        ),
        BackButton(
            state=CreateWishSG.link_to_marketplace
        ),
        state=CreateWishSG.price
    ),
    WishView.preview_wish(
        Cancel(
            I18NFormat('cancel-creation')
        ),
        Button(
            I18NFormat('done'),
            id='done_wish_create',
            on_click=create_wish_handler
        ),
        getter=wish_preview_on_creation_getter,
        state=CreateWishSG.preview
    ),
    on_start=on_start_create_wish_dialog
)
