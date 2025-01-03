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
