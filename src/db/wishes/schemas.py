from typing import Optional

from pydantic import BaseModel

from src.db.users.schemas import User


class Wish(BaseModel):
    id: Optional[int] = None  # на уровне sql авто-генерируется
    # user_id: int
    wish_list_id: int

    name: str
    photo: Optional[str] = None
    description: Optional[str] = None
    link_to_marketplace: Optional[str] = None
    price: Optional[int] = None

    is_booked: bool = False
    booked_by_user_id: Optional[int] = None
    booked_by_user: Optional[User] = None
