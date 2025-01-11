import asyncio

from aiogram import Dispatcher, Bot
from aiogram_dialog import setup_dialogs

from src.config import TOKEN
from src.tgbot.common import start_command
from src.tgbot.main_menu.dialogs import main_dialog
from src.tgbot.middlewares.i18n import TranslatorRunnerMiddleware
from src.tgbot.my_wish_lists.dialogs import my_wish_lists_dialog, create_wish_dialog
from src.tgbot.registration.dialogs import registration_dialog
from src.utils.i18n import create_translator_hub


async def main():
    dp = Dispatcher()
    bot = Bot(token=TOKEN)
    translator_hub = create_translator_hub()

    dp.include_routers(start_command.start_router, registration_dialog, main_dialog, my_wish_lists_dialog, create_wish_dialog)

    dp.update.middleware(TranslatorRunnerMiddleware())

    setup_dialogs(dp)

    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == '__main__':
    asyncio.run(main())

