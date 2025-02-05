import asyncio

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs

from src.config import TOKEN, REDIS_HOST, REDIS_PORT
from src.tgbot.common import start_command
from src.tgbot.friends_wish_list.dialogs import friends_wish_list_dialog
from src.tgbot.main_menu.dialogs import main_dialog
from src.tgbot.middlewares.i18n import TranslatorRunnerMiddleware
from src.tgbot.middlewares.update_user_data import UpdateUserDataMiddleware
from src.tgbot.my_wish_lists.create_wish_list.dialogs import create_wish_list_dialog
from src.tgbot.my_wish_lists.dialogs import my_wish_lists_dialog
from src.tgbot.my_wish_lists.members.dialogs import members_list_dialog
from src.tgbot.my_wish_lists.wish_list_settings.dialogs import wish_list_settings_dialog
from src.tgbot.my_wish_lists.wishes.dialogs import create_wish_dialog, edit_wish_dialog
from src.tgbot.registration.dialogs import registration_dialog
from src.utils.i18n import create_translator_hub

import redis.asyncio as redis


async def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    await r.flushall(asynchronous=True)

    dp = Dispatcher()
    bot = Bot(token=TOKEN)
    translator_hub = create_translator_hub()

    dp.include_routers(
        start_command.start_router,
        registration_dialog,
        main_dialog,
        my_wish_lists_dialog,
        create_wish_dialog,
        edit_wish_dialog,
        members_list_dialog,
        friends_wish_list_dialog,
        create_wish_list_dialog,
        wish_list_settings_dialog
    )

    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.update.middleware(UpdateUserDataMiddleware())

    setup_dialogs(dp)

    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == '__main__':
    asyncio.run(main())

