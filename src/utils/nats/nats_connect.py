import nats
from nats.aio.client import Client
from nats.js import JetStreamContext

from src.config import NATS_HOST, NATS_PORT


async def connect_to_nats() -> tuple[Client, JetStreamContext]:
    nc: Client = await nats.connect(f'nats://{NATS_HOST}:{NATS_PORT}')
    js: JetStreamContext = nc.jetstream()

    return nc, js
