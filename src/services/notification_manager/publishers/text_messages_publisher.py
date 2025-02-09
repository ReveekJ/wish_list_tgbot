from nats.js import JetStreamContext

from src.services.notification_manager.publishers.base import BaseNotificationPublisher
from src.services.notification_manager.schemas.text_message_schema import TextMessage


class TextMessagesNotificationPublisher(BaseNotificationPublisher[TextMessage]):
    def __init__(self, js: JetStreamContext):
        super().__init__(
            js=js,
            subject='Basic.TextMessage.Subject'
        )
