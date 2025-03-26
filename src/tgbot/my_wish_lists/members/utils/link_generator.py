import json

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link

from src.services.security_code_manager.security_code_manager import SecurityCodeManager
from src.tgbot.common.start_schema import StartSchema


async def get_link_for_member_invite(bot: Bot, wish_list_id: int):
    start_schema = StartSchema(
        wlId=wish_list_id,
        sc=SecurityCodeManager().get_security_code(wish_list_id)
    )
    return await create_start_link(bot, start_schema.model_dump_json(), encode=True)
