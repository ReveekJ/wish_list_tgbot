from src.config import LINK_FOR_BOT


def get_link_for_member_invite(wish_list_id: int):
    return f'https://t.me/{LINK_FOR_BOT}?start={wish_list_id}'
