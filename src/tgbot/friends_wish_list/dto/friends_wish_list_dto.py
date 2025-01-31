from typing import Optional

from pydantic import BaseModel

from src.utils.abstract_dialog_data_dto import DialogDataDTO


class FriendsWishListSchema(BaseModel):
    selected_friend_id: Optional[int] = None
    selected_wishlist_id: Optional[int] = None
    selected_wish_id: Optional[int] = None


class FriendsWishListDTO(DialogDataDTO):
    @property
    def data(self) -> FriendsWishListSchema:
        return self._data

    def __init__(self, dialog_manager):
        super().__init__(
            dialog_manager,
            FriendsWishListSchema,
        )
