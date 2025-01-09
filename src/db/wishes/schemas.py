from typing import Optional

from pydantic import BaseModel


class Wish(BaseModel):
    id: int
    user_id: int
    wish_list_id: int

    name: str
    description: Optional[str] = None
    link_to_marketplace: Optional[str] = None
    price: Optional[int] = None
