from pydantic import BaseModel


class WishListMember(BaseModel):
    user_id: int
    wishlist_id: int
