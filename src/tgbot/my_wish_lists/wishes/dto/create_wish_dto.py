from typing import Optional

from aiogram_dialog import DialogManager
from pydantic import BaseModel

from src.utils.abstract_dialog_data_dto import DialogDataDTO


class CreateWishSchema(BaseModel):
    wish_list_id: Optional[int] = None
    name: Optional[str] = None
    photos: Optional[list[str]] = None
    description: Optional[str] = None
    link_to_marketplace: Optional[str] = None
    price: Optional[int] = None

    edit_mode: bool = False


class CreateWishDTO(DialogDataDTO):
    @property
    def data(self) -> CreateWishSchema:
        return self._data

    def __init__(self, dialog_manager: DialogManager):
        super().__init__(
            dialog_manager,
            CreateWishSchema,
        )
