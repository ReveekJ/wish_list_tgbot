from typing import Optional

from aiogram_dialog import DialogManager
from pydantic import BaseModel

from src.utils.abstract_dialog_data_dto import DialogDataDTO


class EditWishSchema(BaseModel):
    wish_id: Optional[int] = None


class EditWishDTO(DialogDataDTO):
    @property
    def data(self) -> EditWishSchema:
        return self._data

    def __init__(self, dialog_manager: DialogManager):
        super().__init__(
            dialog_manager,
            EditWishSchema
        )
