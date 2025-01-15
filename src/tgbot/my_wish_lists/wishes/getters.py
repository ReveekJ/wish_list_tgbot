from aiogram.enums import ContentType
from aiogram.types import User as AiogramUser
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from src.tgbot.my_wish_lists.wishes.dto.create_wish_dto import CreateWishDTO


async def wish_preview_on_creation_getter(event_from_user: AiogramUser, dialog_manager: DialogManager, **kwargs):
    dto = CreateWishDTO(dialog_manager).data

    return {
        'name': dto.name,
        'photos': MediaAttachment(type=ContentType.PHOTO, path=dto.photos[0]) if dto.photos is not None else None,
        'link': dto.link_to_marketplace,
        'price': dto.price,
        'description': dto.description
    }


