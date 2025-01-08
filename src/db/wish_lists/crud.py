from typing import List

from src.db.wish_lists.models import WishListModel
from src.db.wish_lists.schemas import WishList
from src.utils.db_template import DBTemplate, DBParams


class WishListCRUD(DBTemplate):
    def __init__(self):
        super().__init__(
            model_class=WishListModel,
            schema_class=WishList,
            params=DBParams(
                exclude_fields_on_creation={'id'}
            )
        )

    def get_wish_lists_by_user_id(self, user_id: int) -> List[WishList]:
        try:
            res = self._db.query(self._model).filter(WishListModel.owner_id == user_id).scalar().all()
            return [self._schema.model_validate(i) for i in res]
        except AttributeError:  # возникает, когда нет списков
            return []
