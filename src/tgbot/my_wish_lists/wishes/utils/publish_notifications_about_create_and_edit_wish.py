from typing import Literal

from aiogram_dialog import DialogManager
from nats.js import JetStreamContext

from src.db.users.crud import UserCRUD
from src.db.wish_lists.crud import WishListCRUD
from src.db.wishes.schemas import Wish
from src.services.notification_manager.publishers.text_messages_publisher import TextMessagesNotificationPublisher
from src.services.notification_manager.schemas.text_message_schema import TextMessage
from src.tgbot.utils.name_username_concatenate import name_username_concatenate


async def publish_notifications_about_create_and_edit_wish(mode: Literal["create", "edit"], dialog_manager: DialogManager, wish: Wish, wish_list_id: int):
    # рассылаем уведомления
    js: JetStreamContext = dialog_manager.middleware_data.get('js')
    publisher = TextMessagesNotificationPublisher(js)
    messages = []

    with WishListCRUD() as wish_list_crud, UserCRUD() as user_crud:
        wish_list = wish_list_crud.get_obj_by_id(wish_list_id)
        owner_user = user_crud.get_obj_by_id(wish_list.owner_id)

        for user in wish_list.members:
            msg = TextMessage(
                user_id=str(user.id),
                i18n_text='created-new-wish-in-wish-list' if mode == 'create' else 'edited-wish-in-wish-list',
                i18n_params={
                    'username': name_username_concatenate(owner_user),
                    'wish_name': wish.name,
                    'wish_list_name': wish_list.name,
                }
            )
            messages.append(msg)
    await publisher.send_messages_to_users(messages)
