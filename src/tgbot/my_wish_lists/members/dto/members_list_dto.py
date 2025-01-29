from typing import Optional

from aiogram_dialog import DialogManager
from pydantic import BaseModel

from src.utils.abstract_dialog_data_dto import DialogDataDTO


class MembersListSchema(BaseModel):
    wish_list_id: int = None
    selected_member: Optional[int] = None


class MembersListDTO(DialogDataDTO):
    @property
    def data(self) -> MembersListSchema:
        return self._data

    def __init__(self, dialog_manager: DialogManager):
        super().__init__(
            dialog_manager,
            MembersListSchema
        )
