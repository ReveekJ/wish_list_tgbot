import nats
from nats.aio.client import Client
from nats.js import JetStreamContext


async def connect_to_nats(server: list[str] | str) -> tuple[Client, JetStreamContext]:
    nc: Client = await nats.connect(server)
    js: JetStreamContext = nc.jetstream()

    return nc, js
