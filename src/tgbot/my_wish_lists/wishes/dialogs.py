from aiogram_dialog import Dialog
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Button, Back, Next

from src.custom_widgets.i18n_format import I18NFormat
from src.tgbot.my_wish_lists.wishes.getters import wish_preview_on_creation_getter
from src.tgbot.my_wish_lists.wishes.handlers import save_name, save_photos, save_description, save_link_to_marketplace, \
    save_price, on_start_create_wish_dialog, \
    create_wish_handler, set_edit_mode, edit_name, edit_price, edit_link, edit_description, \
    edit_photo, on_start_edit_wish_dialog
from src.tgbot.my_wish_lists.wishes.states import CreateWishSG, EditWishSG
from src.tgbot.shared.wish_edit_dialog import WishEdit
from src.tgbot.shared.wish_view import WishView

create_wish_dialog = Dialog(
    WishEdit.name_window(
        Cancel(
            I18NFormat('back')
        ),
        handler=save_name,
        state=CreateWishSG.name
    ),
    WishEdit.photo_window(
    Next(
            I18NFormat('skip-step'),
        ),
        Back(
            I18NFormat('back')
        ),
        handler=save_photos,
        state=CreateWishSG.photos
    ),
    WishEdit.description_window(
    Next(
            I18NFormat('skip-step'),
        ),
        Back(
            I18NFormat('back')
        ),
        handler=save_description,
        state=CreateWishSG.description
    ),
    WishEdit.link_window(
        Next(
            I18NFormat('skip-step'),
        ),
        Back(
            I18NFormat('back')
        ),
        handler=save_link_to_marketplace,
        state=CreateWishSG.link_to_marketplace
    ),
    WishEdit.price_window(
        Next(
            I18NFormat('skip-step'),
        ),
        Back(
            I18NFormat('back')
        ),
        handler=save_price,
        state=CreateWishSG.price
    ),
    WishView.preview_wish(
        SwitchTo(
            I18NFormat('edit-name'),
            id='edit_name',
            state=CreateWishSG.name,
            on_click=set_edit_mode
        ),
        SwitchTo(
            I18NFormat('edit-photo'),
            id='edit_photo',
            state=CreateWishSG.photos,
            on_click=set_edit_mode
        ),
        SwitchTo(
            I18NFormat('edit-description'),
            id='edit_description',
            state=CreateWishSG.description,
            on_click=set_edit_mode
        ),
        SwitchTo(
            I18NFormat('edit-link-to-marketplace'),
            id='edit_link_to_marketplace',
            state=CreateWishSG.link_to_marketplace,
            on_click=set_edit_mode
        ),
        SwitchTo(
            I18NFormat('edit-price'),
            id='edit_price',
            state=CreateWishSG.price,
            on_click=set_edit_mode
        ),
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
# TODO: добавить кнопку "сделать значение пустым"
edit_wish_dialog = Dialog(
    WishEdit.name_window(
        Cancel(
            I18NFormat('back')
        ),
        handler=edit_name,
        state=EditWishSG.name
    ),
    WishEdit.photo_window(
        Cancel(
            I18NFormat('back')
        ),
        handler=edit_photo,
        state=EditWishSG.photos
    ),
    WishEdit.description_window(
        Cancel(
            I18NFormat('back')
        ),
        handler=edit_description,
        state=EditWishSG.description
    ),
    WishEdit.link_window(
        Cancel(
            I18NFormat('back')
        ),
        handler=edit_link,
        state=EditWishSG.link_to_marketplace
    ),
    WishEdit.price_window(
        Cancel(
            I18NFormat('back')
        ),
        handler=edit_price,
        state=EditWishSG.price
    ),
    on_start=on_start_edit_wish_dialog,
)
