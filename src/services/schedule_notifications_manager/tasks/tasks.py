import datetime

from nats.js import JetStreamContext
from pydantic import BaseModel
from taskiq.scheduler.created_schedule import CreatedSchedule

from src.db.users.crud import UserCRUD
from src.db.wish_lists.crud import WishListCRUD
from src.services.notification_manager.publishers.text_messages_publisher import TextMessagesNotificationPublisher
from src.services.notification_manager.schemas.text_message_schema import TextMessage
from src.services.schedule_notifications_manager.taskiq_brokers.broker import broker, redis_source
from src.utils.nats.nats_connect import connect_to_nats
from src.utils.singleton_metaclass import Singleton


class BirthdateNotificationConfig(BaseModel):
    user_id: int
    birthdate: datetime.date
    notification_time: datetime.time = datetime.time(hour=12, minute=0)
    i18n_text: str
    i18n_params: dict[str, str]


class BirthdateNotificationManager(metaclass=Singleton):
    js: JetStreamContext = None

    @staticmethod
    @broker.task
    async def __birthdate_notifications_task(config: BirthdateNotificationConfig):
        nc, js = await connect_to_nats()

        with UserCRUD() as user_crud:
            user = user_crud.get_obj_by_id(config.user_id)
            if user.is_blocked:
                await redis_source.delete_schedule()
        with WishListCRUD() as crud:
            wish_lists = crud.get_wish_lists_by_user_id(config.user_id)
            users_to_notify = []

            for wish_list in wish_lists:
                users_to_notify += wish_list.members

        publisher = TextMessagesNotificationPublisher(
            js=js
        )
        messages = []
        for user in users_to_notify:
            messages.append(
                TextMessage(
                    user_id=user.id,
                    i18n_text=config.i18n_text,
                    i18n_params=config.i18n_params,
                )
            )

        await publisher.send_messages_to_users(messages)

    async def schedule_notifications(self, config: BirthdateNotificationConfig):
        schedule: CreatedSchedule = await self.__birthdate_notifications_task.schedule_by_cron(
            redis_source,
            f'{config.notification_time.minute} {config.notification_time.hour} {config.birthdate.day} */{config.birthdate.month} *',
            config
        )
