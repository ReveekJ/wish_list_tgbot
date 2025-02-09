from aiogram import Bot
from fluentogram import TranslatorHub
from nats.aio.client import Client
from nats.js import JetStreamContext

from src.services.notification_manager.consumers.text_messages_consumer import TextMessagesNotificationConsumer


async def start_consumers(
    nc: Client,
    js: JetStreamContext,
    bot: Bot,
    translator_hub: TranslatorHub,
):
    text_messages_consumer = TextMessagesNotificationConsumer(nc=nc, js=js, bot=bot, translator_hub=translator_hub)

    await text_messages_consumer.start()
