import urllib.parse
from src.config import LINK_FOR_BOT
from src.tgbot.common.start_schema import StartSchema


def get_link_for_member_invite(wish_list_id: int):
    start_schema = StartSchema(
        wish_list_id=wish_list_id,
    )
    return f'{LINK_FOR_BOT}?start={urllib.parse.quote(start_schema.model_dump_json())}'
