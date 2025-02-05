from typing import Dict, Any, Optional

from src.db.cache_db_binds import CACHE_WISH_DB, CACHE_WISH_LIST_DB
from src.db.wishes.models import WishModel
from src.db.wishes.schemas import Wish
from src.utils.cache_manager import CacheManager
from src.utils.db_template import DBTemplate, DBParams


class WishCRUD(DBTemplate[WishModel, Wish]):
    def __init__(self):
        super().__init__(
            model_class=WishModel,
            schema_class=Wish,
            params=DBParams(
                exclude_fields_on_creation={'id'},
                cache_redis_db=CACHE_WISH_DB
            )
        )

    @CacheManager(CACHE_WISH_LIST_DB).reset_cache('wish_list_id')
    @CacheManager(CACHE_WISH_DB, Wish).save_cache_from_db()
    def create(self, obj: Wish) -> Wish:
        return super().create(obj)

    @CacheManager(CACHE_WISH_LIST_DB).reset_cache('wish_list_id')
    @CacheManager(CACHE_WISH_DB, Wish).save_cache_from_db()
    def update(self, obj_id: int, obj_data: Dict[str, Any]) -> Optional[Wish]:
        return super().update(obj_id, obj_data)

    @CacheManager(CACHE_WISH_LIST_DB).reset_cache('wish_list_id')
    @CacheManager(CACHE_WISH_DB).reset_cache()
    def delete(self, obj_id: int) -> Optional[Wish]:
        return super().delete(obj_id)

    @CacheManager(CACHE_WISH_DB, Wish).save_cache_from_db()
    def get_obj_by_id(self, obj_id: int) -> Optional[Wish]:
        return super().get_obj_by_id(obj_id)
