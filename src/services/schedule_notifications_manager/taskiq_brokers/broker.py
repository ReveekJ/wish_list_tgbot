from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker, RedisScheduleSource

from src.config import REDIS_HOST, REDIS_PORT, REDIS_TASKIQ_DB

broker = ListQueueBroker(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_TASKIQ_DB}")

redis_source = RedisScheduleSource(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_TASKIQ_DB}")

scheduler = TaskiqScheduler(broker, sources=[redis_source])
