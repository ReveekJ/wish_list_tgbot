import asyncio
from calendar import mdays

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from fluentogram import TranslatorRunner, TranslatorHub
from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext

from src.db.users.crud import UserCRUD
from src.services.notification_manager.consumers.base import BaseNotificationConsumer
from src.services.notification_manager.schemas.text_message_schema import TextMessage


class TextMessagesNotificationConsumer(BaseNotificationConsumer[TextMessage]):
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            bot: Bot,
            translator_hub: TranslatorHub,
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
        self.__translator_buh = translator_hub

    async def on_message(self, msg: Msg):
        message: TextMessage = self.message_schema.model_validate(msg.headers)

        with UserCRUD() as crud:
            user = crud.get_obj_by_id(int(message.user_id))

        if user.is_blocked:
            await msg.ack()
            return

        i18n = self.__translator_buh.get_translator_by_locale(user.language_code)
        try:
            await self.bot.send_message(chat_id=message.user_id, text=i18n.get(message.i18n_text, **message.i18n_params))
            await msg.ack()
        except TelegramRetryAfter as e:
            await msg.nak(e.retry_after)
