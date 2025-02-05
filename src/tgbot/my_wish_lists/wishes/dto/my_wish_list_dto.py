import json
from typing import Optional

from aiogram_dialog import DialogManager
from pydantic import BaseModel

from src.utils.abstract_dialog_data_dto import DialogDataDTO


class MyWishListsSchema(BaseModel):
    selected_wish_list_id: Optional[int] = None
    selected_wish: Optional[int] = None


class MyWishListsDTO(DialogDataDTO):
    def __init__(self, dialog_manager: DialogManager):
        super().__init__(
            dialog_manager,
            MyWishListsSchema
        )

    @property
    def data(self) -> MyWishListsSchema:
        return self._data
