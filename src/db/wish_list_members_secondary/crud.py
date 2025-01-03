from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import select

from src.db.wish_list_members_secondary.models import WishListMembersModel
from src.db.wish_list_members_secondary.schemas import WishListMember
from src.utils.db_template import DBTemplate, DBParams


class WishListMembersSecondaryCRUD(DBTemplate):
    def __init__(self):
        super().__init__(
            model_class=WishListMembersModel,
            schema_class=WishListMember,
        )
        self._model: WishListMembersModel

    def get(self, obj_id: int) -> Optional[BaseModel]:
        raise NotImplementedError()

    def get_all(self, skip: int = 0, limit: int = 10) -> List[BaseModel]:
        raise NotImplementedError()

    def delete(self, obj_id: int) -> Optional[BaseModel]:
        raise NotImplementedError()

    def update(self, obj_id: int, obj_data: dict) -> Optional[BaseModel]:
        raise NotImplementedError()

    def get_wish_lists_id(self, user_id: int) -> List[int]:
        query = select(self._model).where(self._model.user_id == user_id)
        res: list[WishListMember] = [self._schema.model_validate(i, from_attributes=True) for i in self._db.execute(query).scalars().all()]

        return [i.wishlist_id for i in res]

    def delete_pair(self, user_id: int, wishlist_id: int) -> Optional[WishListMembersModel]:
        obj = self._db.query(self._model).filter(self._model.user_id == user_id, self._model.wishlist_id == wishlist_id).first()
        if obj:
            self._db.delete(obj)
            self._db.commit()
            return self._schema.model_validate(obj, from_attributes=True)
        return None
