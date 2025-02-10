import json
from typing import Optional, Literal, Any, Self

from pydantic import BaseModel, field_validator
from pydantic.main import IncEx


class TextMessage(BaseModel):
    user_id: str
    i18n_text: str
    i18n_params: Optional[dict[str, str]] = {}

    def model_dump(
        self,
        *,
        mode: Literal['json', 'python'] | str = 'python',
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal['none', 'warn', 'error'] = True,
        serialize_as_any: bool = False,
    ) -> dict[str, str]:
        res = super().model_dump(
            mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, round_trip=round_trip, warnings=warnings, serialize_as_any=serialize_as_any
        )
        res['i18n_params'] = json.dumps(res['i18n_params'])
        return res

    @field_validator('i18n_params', mode='before')
    @classmethod
    def i18n_params_validator(cls, v):
        if isinstance(v, str):
            v = json.loads(v)

        return v
