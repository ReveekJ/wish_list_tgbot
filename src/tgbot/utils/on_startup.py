import redis
from aiogram import Dispatcher
from dishka import make_async_container, Scope, AsyncContainer
from dishka.integrations.aiogram import AiogramProvider, setup_dishka
from fluentogram import TranslatorHub
from nats.js import JetStreamContext
from nats.js.api import StreamConfig, RetentionPolicy, StorageType
from nats.js.errors import NotFoundError

from src.config import REDIS_TASKIQ_DB, REDIS_AIOGRAM_DB, REDIS_USER_SCHEDULES_DB, REDIS_SECURITY_CODE_DB, REDIS_HOST, \
    REDIS_PORT, CACHE_LAST_MESSAGE_ID
from src.dependencies.service_provider import ServiceProvider
from src.services.redis_last_message_id_cache import RedisLastMessageIdCache
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

    @staticmethod
    def flush_redis():
        for db in range(0, 16):
            if db in [REDIS_TASKIQ_DB, REDIS_AIOGRAM_DB, REDIS_USER_SCHEDULES_DB, REDIS_SECURITY_CODE_DB, CACHE_LAST_MESSAGE_ID]:
                continue
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=db)
            r.flushdb(asynchronous=True)

    @staticmethod
    def dishka_setup(dp: Dispatcher) -> AsyncContainer:
        aiogram_provider = AiogramProvider(scope=Scope.APP)
        aiogram_provider.provide(RedisLastMessageIdCache)

        container = make_async_container(aiogram_provider, ServiceProvider())
        setup_dishka(container=container, router=dp, auto_inject=True)

        return container
