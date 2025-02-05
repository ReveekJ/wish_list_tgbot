from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import select

from src.db.cache_db_binds import CACHE_WISH_LIST_MEMBERS_SECONDARY_DB, CACHE_WISH_LIST_DB, CACHE_USER_DB
from src.db.users.schemas import User
from src.db.wish_list_members_secondary.models import WishListMembersModel
from src.db.wish_list_members_secondary.schemas import WishListMember
from src.utils.cache_manager import CacheManager
from src.utils.db_template import DBTemplate, DBParams


class WishListMembersSecondaryCRUD(DBTemplate[WishListMembersModel, WishListMember]):

    def __init__(self):
        super().__init__(
            model_class=WishListMembersModel,
            schema_class=WishListMember,
            params=DBParams(cache_redis_db=CACHE_WISH_LIST_MEMBERS_SECONDARY_DB)
        )
        self._model_class: WishListMembersModel

    # @staticmethod
    # def _reset_cache(func):
    #     def inner(*args, **kwargs):
    #         res = func(*args, **kwargs)
    #         if isinstance(res, WishListMember):
    #             CacheManager._delete_cache_in_another_db(CACHE_USER_DB, res.user_id)
    #             CacheManager._delete_cache_in_another_db(CACHE_WISH_LIST_DB, res.wishlist_id)
    #     return inner

    @CacheManager(CACHE_USER_DB, User).reset_cache('user_id')
    @CacheManager(CACHE_WISH_LIST_DB, User).reset_cache('wishlist_id')
    def create(self, obj: WishListMember) -> WishListMember:
        return super().create(obj)

    def get_obj_by_id(self, obj_id: int) -> Optional[BaseModel]:
        raise NotImplementedError()

    def get_all(self, skip: int = 0, limit: int = 10) -> List[BaseModel]:
        raise NotImplementedError()

    def delete(self, obj_id: int) -> Optional[BaseModel]:
        raise NotImplementedError()

    def update(self, obj_id: int, obj_data: dict) -> Optional[BaseModel]:
        raise NotImplementedError()

    def does_pair_exists(self, user_id: int, wishlist_id: int) -> bool:
        query = select(self._model_class.user_id).where(self._model_class.user_id == user_id, self._model_class.wishlist_id == wishlist_id)
        res = self._db.execute(query).scalars().all()

        return True if res else False

    def get_wish_lists_id(self, user_id: int) -> List[int]:
        query = select(self._model_class).where(self._model_class.user_id == user_id)
        res: list[WishListMember] = [self._schema_class.model_validate(i, from_attributes=True) for i in self._db.execute(query).scalars().all()]

        return [i.wishlist_id for i in res]

    @CacheManager(CACHE_USER_DB, User).reset_cache('user_id')
    @CacheManager(CACHE_WISH_LIST_DB, User).reset_cache('wishlist_id')
    def delete_pair(self, user_id: int, wishlist_id: int) -> Optional[WishListMembersModel]:
        obj = self._db.query(self._model_class).filter(self._model_class.user_id == user_id, self._model_class.wishlist_id == wishlist_id).first()
        if obj:
            self._db.delete(obj)
            self._db.commit()
            return self._schema_class.model_validate(obj, from_attributes=True)
        return None
