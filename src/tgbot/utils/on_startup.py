from nats.js import JetStreamContext
from nats.js.api import StreamConfig, RetentionPolicy, StorageType
from nats.js.errors import NotFoundError

from src.services.schedule_notifications_manager.taskiq_brokers.broker import broker, redis_source, scheduler
from src.services.schedule_notifications_manager.tasks.tasks import BirthdateNotificationManager


class OnStartupActions:
    async def setup_notifications(self, js: JetStreamContext):
        await broker.startup()
        await redis_source.startup()
        await scheduler.startup()

        await self.__setup_birthdate(js)

    @staticmethod
    async def __setup_birthdate(js: JetStreamContext):
        birthdate = BirthdateNotificationManager()
        birthdate.js = js

    @staticmethod
    async def run_nuts_migrations(js: JetStreamContext):
        streams = [
            StreamConfig(
                name="Basic_TextMessage_Stream",
                subjects=[
                    'Basic.TextMessage.Subject'
                ],
                retention=RetentionPolicy.INTEREST,  # Политика удержания
                max_bytes=300 * 1024 * 1024,  # 300 MiB
                max_msg_size=10 * 1024 * 1024,  # 10 MiB
                storage=StorageType.FILE,  # Хранение сообщений на диске
                allow_direct=False,  # Разрешение получать сообщения без создания консьюмера
            )
        ]

        for stream in streams:
            try:
                await js.delete_stream(stream.name)
            except NotFoundError:
                pass
            await js.add_stream(stream)
