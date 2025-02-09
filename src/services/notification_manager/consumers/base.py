from abc import ABC, abstractmethod
from typing import Type

from aiogram import Bot
from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext
from typing_extensions import Generic

from src.services.notification_manager.publishers.base import MessageSchema


class BaseNotificationConsumer(Generic[MessageSchema], ABC):
    def __init__(
            self,
            nc: Client,
            js: JetStreamContext,
            bot: Bot,
            subject: str,
            stream: str,
            durable_name: str,
            message_schema: Type[MessageSchema]
    ):
        self.stream_sub = None
        self.nc = nc
        self.js = js
        self.bot = bot
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name
        self.message_schema = message_schema

    async def start(self) -> None:
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            manual_ack=True
        )

    @abstractmethod
    async def on_message(self, msg: Msg):
        ...

    async def unsubscribe(self) -> None:
        if self.stream_sub:
            await self.stream_sub.unsubscribe()
