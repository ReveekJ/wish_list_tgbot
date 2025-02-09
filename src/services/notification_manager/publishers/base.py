from typing import List, Generic

from nats.js import JetStreamContext

from src.services.notification_manager.schemas.generics import MessageSchema


class BaseNotificationPublisher(Generic[MessageSchema]):
    def __init__(
            self,
            js: JetStreamContext,
            subject: str
    ):
        self.__js = js
        self.__subject = subject

    async def send_messages_to_users(
            self,
            messages: List[MessageSchema]
    ):
        for message in messages:
            headers = message.model_dump()

            await self.__js.publish(subject=self.__subject, headers=headers)
