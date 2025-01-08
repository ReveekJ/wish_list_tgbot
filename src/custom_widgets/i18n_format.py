from typing import Dict

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text, Format
from fluentogram import TranslatorRunner


class I18NFormat(Format):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when)
        self.text = text

    async def _render_text(self, data: Dict, manager: DialogManager) -> str:
        res = await super()._render_text(data, manager)

        i18n: TranslatorRunner = manager.middleware_data.get('i18n')
        value = i18n.get(res, **data)
        if value is None:
            raise KeyError(f'translation key = "{res}" not found')
        return value
