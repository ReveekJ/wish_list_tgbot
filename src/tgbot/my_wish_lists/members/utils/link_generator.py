import json

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link

from src.tgbot.common.start_schema import StartSchema


async def get_link_for_member_invite(bot: Bot, wish_list_id: int):
    start_schema = StartSchema(
        wish_list_id=wish_list_id,
    )
    return await create_start_link(bot, json.dumps(start_schema.model_dump()), encode=True)