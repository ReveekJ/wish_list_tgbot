from typing import Optional

from pydantic import BaseModel


class Wish(BaseModel):
    id: Optional[int] = None  # на уровне sql авто-генерируется
    # user_id: int
    wish_list_id: int

    name: str
    photo: Optional[str] = None
    description: Optional[str] = None
    link_to_marketplace: Optional[str] = None
    price: Optional[int] = None
