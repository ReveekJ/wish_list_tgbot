import datetime
from typing import Optional

from aiogram_dialog import DialogManager
from pydantic import BaseModel

from src.db.users.enums import GenderEnum
from src.utils.abstract_dialog_data_dto import DialogDataDTO


class RegistrationSchema(BaseModel):
    selected_birthdate: Optional[datetime.date] = None
    gender: Optional[GenderEnum] = None


class RegistrationDTO(DialogDataDTO):
    def __init__(self, dialog_manager: DialogManager):
        super().__init__(
            dialog_manager,
            RegistrationSchema
        )

    @property
    def data(self) -> RegistrationSchema:
        return self._data
