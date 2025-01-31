from typing import Optional

from pydantic import BaseModel



class WishList(BaseModel):
    id: Optional[int] = None
    owner_id: int
    name: str

    members: list["User"] = []
    wishes: list["Wish"] = []

    class Config:
        from_attributes = True


from src.db.users.schemas import User
from src.db.wishes.schemas import Wish
