from abc import ABC, abstractmethod
from typing import Type

from aiogram_dialog import DialogManager
from pydantic import BaseModel


class DialogDataDTO(ABC):
    def __init__(self, dialog_manager: DialogManager, data_schema: Type[BaseModel]):
        self._dialog_manager = dialog_manager
        self._data_schema = data_schema
        self._data = data_schema.model_validate_json(self._dialog_manager.dialog_data.get('dto', '{}'))

    @property
    @abstractmethod
    def data(self) -> BaseModel:
        pass

    @data.setter
    def data(self, value: BaseModel):
        if issubclass(value, BaseModel):
            self._data = value
        else:
            raise ValueError(f'{value.__class__.__name__} is not a subclass of BaseModel')

    def save_to_dialog_manager(self, dialog_manager: DialogManager):
        dialog_manager.dialog_data['dto'] = self.data.model_dump_json()
        self._dialog_manager = dialog_manager  # на всякий случай
