from typing import Optional

from pydantic import BaseModel


class TextMessage(BaseModel):
    user_id: str
    i18n_text: str
    i18n_params: Optional[dict[str, str]] = {}
