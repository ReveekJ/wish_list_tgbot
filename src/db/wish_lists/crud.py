from typing import List

from sqlalchemy import select

from src.db.wish_lists.models import WishListModel
from src.db.wish_lists.schemas import WishList
from src.utils.db_template import DBTemplate, DBParams


class WishListCRUD(DBTemplate[WishListModel, WishList]):
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
            res = self._db.query(self._model_class).filter(WishListModel.owner_id == user_id).all()
            return [self._schema_class.model_validate(i, from_attributes=True) for i in res]
        except AttributeError:  # возникает, когда нет списков
            return []

    def does_wish_list_exist_by_user_id_n_wish_list_name(self, user_id: int, wish_list_name: str) -> bool:
        query = select(self._model_class).where(self._model_class.owner_id == user_id, self._model_class.name == wish_list_name)
        res = self._db.execute(query).scalars().all()

        return True if res else False
