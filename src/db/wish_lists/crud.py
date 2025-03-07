from typing import List, Dict, Any, Optional

from sqlalchemy import select

from src.db.cache_db_binds import CACHE_WISH_LIST_DB, CACHE_USER_DB
from src.db.users.models import UserModel
from src.db.wish_list_members_secondary.models import WishListMembersModel
from src.db.wish_lists.models import WishListModel
from src.db.wish_lists.schemas import WishList
from src.utils.cache_manager import CacheManager
from src.utils.db_template import DBTemplate, DBParams


class WishListCRUD(DBTemplate[WishListModel, WishList]):
    def __init__(self):
        super().__init__(
            model_class=WishListModel,
            schema_class=WishList,
            params=DBParams(
                exclude_fields_on_creation={'id'},
                cache_redis_db=CACHE_WISH_LIST_DB
            )
        )

    def get_wish_lists_which_user_subscribed(self, subscriber_id: int, wish_list_owner_id: int) -> List[WishListModel]:
        query = (select(WishListModel)
                 .join(UserModel, WishListModel.owner_id == UserModel.id)
                 .join(WishListMembersModel)
                 .filter(UserModel.id == wish_list_owner_id, WishListMembersModel.user_id == subscriber_id))
        res = self._db.execute(query).scalars().all()

        return [WishList.model_validate(i, from_attributes=True) for i in res]

    @CacheManager(CACHE_USER_DB).reset_cache('owner_id')
    @CacheManager(CACHE_WISH_LIST_DB, WishList).save_cache_from_db()
    def create(self, obj: WishList) -> WishList:
        return super().create(obj)

    @CacheManager(CACHE_USER_DB).reset_cache('owner_id')
    @CacheManager(CACHE_WISH_LIST_DB, WishList).save_cache_from_db()
    def update(self, obj_id: int, obj_data: Dict[str, Any]) -> Optional[WishList]:
        return super().update(obj_id, obj_data)

    @CacheManager(CACHE_USER_DB).reset_cache('owner_id')
    @CacheManager(CACHE_WISH_LIST_DB).reset_cache()
    def delete(self, obj_id: int) -> Optional[WishList]:
        return super().delete(obj_id)
    
    @CacheManager(CACHE_WISH_LIST_DB, WishList).save_cache_from_db()
    def get_obj_by_id(self, obj_id: int) -> Optional[WishList]:
        return super().get_obj_by_id(obj_id)

    def get_wish_lists_by_user_id(self, user_id: int) -> List[WishList]:
        try:
            res = self._db.query(self._model_class).filter(WishListModel.owner_id == user_id).all()
            return [self._schema_class.model_validate(i, from_attributes=True) for i in res]
        except AttributeError:  # возникает, когда нет списков
            return []

    def does_wish_list_exist_by_user_id_n_wish_list_name(self, user_id: int, wish_list_name: str) -> bool:
        query = select(self._model_class).where(self._model_class.owner_id == user_id, self._model_class.name == wish_list_name)
        res = self._db.execute(query).scalars().all()

        return True if res else False
