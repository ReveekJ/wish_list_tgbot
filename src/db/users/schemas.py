import datetime
from typing import Optional

from pydantic import BaseModel

from src.db.users.enums import GenderEnum


class User(BaseModel):
    id: int

    birthdate: datetime.date
    gender: GenderEnum
    name: str
    username: str

    own_wish_lists: Optional[list["WishList"]] = []
    member_wish_lists: Optional[list["WishList"]] = []

    class Config:
        from_attributes = True



from src.db.wish_lists.schemas import WishList
