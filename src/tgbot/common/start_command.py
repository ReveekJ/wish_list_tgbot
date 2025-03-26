import json

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.payload import decode_payload
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.exceptions import NoContextError
from dishka import FromDishka
from fluentogram import TranslatorRunner

from src.db.users.crud import UserCRUD
from src.db.wish_list_members_secondary.crud import WishListMembersSecondaryCRUD
from src.db.wish_list_members_secondary.schemas import WishListMember
from src.db.wish_lists.crud import WishListCRUD
from src.services.redis_last_message_id_cache import RedisLastMessageIdCache
from src.services.security_code_manager.security_code_manager import SecurityCodeManager
from src.tgbot.common.start_schema import StartSchema
from src.tgbot.main_menu.states import MainMenuSG
from src.tgbot.registration.states import RegistrationSG

start_router = Router()


@start_router.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager, i18n: TranslatorRunner, bot: Bot, r: FromDishka[RedisLastMessageIdCache]):
    data = message.text.split()[-1]

    # сбрасываем диалоги
    flag = True
    while flag:
        try:
            await dialog_manager.done(show_mode=ShowMode.EDIT)
        except NoContextError:
            flag = False

    # удаляем это сообщение для красоты
    last_message_id = r.get(message.from_user.id)
    if last_message_id:
        await bot.delete_message(message.chat.id, last_message_id)
        r.delete(message.from_user.id)

    # Если пользователь не зарегистрирован - отправить на регистрацию
    with UserCRUD() as user_crud:
        if user_crud.get_obj_by_id(message.from_user.id) is None:
            await message.answer(i18n.get('greeting-message', username=message.from_user.full_name))
            await dialog_manager.start(RegistrationSG.birthdate)
            return

    if data != "/start": #  пользователь зарегистрирован и он перешел по ссылке на вступление в список желаний
        try:
            loaded_json = json.loads(decode_payload(data))
            loaded_data = StartSchema.model_validate(loaded_json)
            del loaded_json
        except Exception as e:  # будет ошибка валидации, если ссылка не верна
            await message.answer(i18n.get('security-code-invalid'))
            await dialog_manager.start(MainMenuSG.main_menu)
            return

        if not SecurityCodeManager().check_security_code(loaded_data.sc, loaded_data.wlId):
            await message.answer(i18n.get('security-code-invalid'))
            await dialog_manager.start(MainMenuSG.main_menu)
            return

        with WishListCRUD() as wish_list_crud:
            wish_list = wish_list_crud.get_obj_by_id(loaded_data.wlId)

        if wish_list.owner_id == message.from_user.id:
            await message.answer(i18n.get('you-are-owner-of-wish-list'))
            await dialog_manager.start(MainMenuSG.main_menu)
            return

        with WishListMembersSecondaryCRUD() as members_secondary_crud:
            if members_secondary_crud.does_pair_exists(message.from_user.id, loaded_data.wlId):  # если пользователь уже в этом списке желаний
                await message.answer(i18n.get('already-in-wish-list', wishlist_name=wish_list.name))
                await dialog_manager.start(MainMenuSG.main_menu)
                return

            pair = WishListMember(
                user_id=message.from_user.id,
                wishlist_id=loaded_data.wlId
            )
            members_secondary_crud.create(pair)


        await message.answer(i18n.get('successfully-joined-to-wishlist', wishlist_name=wish_list.name))
        await dialog_manager.start(MainMenuSG.main_menu)
        return

    await dialog_manager.start(MainMenuSG.main_menu) # пользователь зарегистрирован, просто нажал на кнопку старт и просто это нужно делать всегда
