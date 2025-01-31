from typing import Optional

from aiogram_dialog import DialogManager
from pydantic import BaseModel

from src.utils.abstract_dialog_data_dto import DialogDataDTO


class WishListSettingSchema(BaseModel):
    wish_list_id: Optional[int] = None
    new_name: Optional[str] = None


class WishListSettingsDTO(DialogDataDTO):
    @property
    def data(self) -> WishListSettingSchema:
        return self._data

    def __init__(self, dialog_manager: DialogManager):
        super().__init__(
            dialog_manager,
            WishListSettingSchema
        )
