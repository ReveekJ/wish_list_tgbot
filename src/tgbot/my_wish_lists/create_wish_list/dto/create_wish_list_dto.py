from typing import Optional

from aiogram_dialog import DialogManager
from pydantic import BaseModel

from src.utils.abstract_dialog_data_dto import DialogDataDTO


class CreateWishListSchema(BaseModel):
    name: Optional[str] = None


class CreateWishListDTO(DialogDataDTO):
    @property
    def data(self) -> CreateWishListSchema:
        return self._data

    def __init__(self, dialog_manager: DialogManager):
        super().__init__(
            dialog_manager,
            CreateWishListSchema,
        )
        