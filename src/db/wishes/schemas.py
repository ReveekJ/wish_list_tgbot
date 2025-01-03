from pydantic import BaseModel


class Wish(BaseModel):
    id: int
    user_id: int
    wish_list_id: int
