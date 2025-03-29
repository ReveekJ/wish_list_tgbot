from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from aiogram.types import User as AiogramUser, Chat
from aiogram_dialog import StartMode, ShowMode
from aiogram_dialog.manager.bg_manager import BgManager
from dishka import AsyncContainer
from fluentogram import TranslatorHub
from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

from src.db.users.crud import UserCRUD
from src.services.notification_manager.consumers.base import BaseNotificationConsumer
from src.services.notification_manager.schemas.text_message_schema import TextMessage
from src.services.redis_last_message_id_cache import RedisLastMessageIdCache
from src.tgbot.main_menu.dialogs import main_dialog
from src.tgbot.main_menu.states import MainMenuSG


class TextMessagesNotificationConsumer(BaseNotificationConsumer[TextMessage]):
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            bot: Bot,
            translator_hub: TranslatorHub,
            di_container: AsyncContainer
    ):
        super().__init__(
            nc=nc,
            js=js,
            bot=bot,
            subject='Basic.TextMessage.Subject',
            stream='Basic_TextMessage_Stream',
            durable_name=self.__class__.__name__,
            message_schema=TextMessage
        )
        self.__translator_hub = translator_hub
        self.__di_container = di_container

    async def on_message(self, msg: Msg):
        message: TextMessage = self.message_schema.model_validate(msg.headers)

        with UserCRUD() as crud:
            user = crud.get_obj_by_id(int(message.user_id))

        if user.is_blocked:
            await msg.ack()
            return

        i18n = self.__translator_hub.get_translator_by_locale(user.language_code)
        try:
            await self.bot.send_message(chat_id=message.user_id, text=i18n.get(message.i18n_text, **message.i18n_params))

            # удаляем последнее сообщение у пользователя, для красоты
            r = await self.__di_container.get(RedisLastMessageIdCache)
            last_message_id = await r.get(int(message.user_id))
            try:
                await self.bot.delete_message(chat_id=message.user_id, message_id=last_message_id)
            except TelegramBadRequest:
                pass

            # отправляем основной диалог
            aiogram_user = AiogramUser(id=user.id, language_code=user.language_code, is_bot=False, first_name=user.name)
            chat = Chat(id=user.id, type='private')
            bg_manager = BgManager(user=aiogram_user, chat=chat, bot=self.bot, router=main_dialog, intent_id=None, stack_id="")
            await bg_manager.start(
                MainMenuSG.main_menu,
                mode=StartMode.RESET_STACK,
                show_mode=ShowMode.SEND
            )

            # обновляем last_message_id
            await r.set(int(message.user_id), int(last_message_id) + int('2'))

            # отмечаем сообщение обработанным
            await msg.ack()
        except TelegramRetryAfter as e:
            await msg.nak(e.retry_after)
