from pydantic import BaseModel



class User(BaseModel):
    id: int

    own_wish_lists: list["WishList"]
    member_wish_lists: list["WishList"]

    class Config:
        from_attributes = True



from src.db.wish_lists.schemas import WishList
