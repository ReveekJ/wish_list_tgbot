from nats.js import JetStreamContext
from nats.js.api import StreamConfig, RetentionPolicy, StorageType


async def run_nuts_migrations(js: JetStreamContext):
    stream_config = StreamConfig(
        name="Basic_TextMessage_Stream",
        subjects=[
            'Basic.TextMessage.Subject'
        ],
        retention=RetentionPolicy.LIMITS,  # Политика удержания
        max_bytes=300 * 1024 * 1024,  # 300 MiB
        max_msg_size=10 * 1024 * 1024,  # 10 MiB
        storage=StorageType.FILE,  # Хранение сообщений на диске
        allow_direct=False,  # Разрешение получать сообщения без создания консьюмера
    )

    await js.add_stream(stream_config)
