import json

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.db.users.crud import UserCRUD
from src.tgbot.main_menu.states import MainMenuSG
from src.tgbot.registration.states import RegistrationSG
from src.tgbot.common.start_schema import StartSchema

start_router = Router()


@start_router.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager):
    data = message.text.split()[-1]
    # pprint(message.model_dump())

    if data == "/start":
        with UserCRUD() as crud:
            if crud.get_obj_by_id(message.from_user.id) is None:
                # TODO: отправить приветственное сообщение
                # await message.answer()
                await dialog_manager.start(RegistrationSG.birthdate)
            else:
                await dialog_manager.start(MainMenuSG.main_menu)
    else:
        loaded_json = json.loads(data)
        loaded_data = StartSchema.model_validate(loaded_json)

        # TODO: здесь нужно сделать юзера мембером вишлиста