import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from src.db.users.enums import GenderEnum


class User(BaseModel):
    id: int

    birthdate: datetime.date
    gender: GenderEnum
    name: str
    username: str
    language_code: str
    is_blocked: bool = False

    # own_wish_lists: Optional[list["WishList"]] = []
    # member_wish_lists: Optional[list["WishList"]] = []

    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, value) -> str:
        if value is None:
            return ''
        return value

    class Config:
        from_attributes = True



from src.db.wish_lists.schemas import WishList
