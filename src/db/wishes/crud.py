from src.db.wishes.models import WishModel
from src.db.wishes.schemas import Wish
from src.utils.db_template import DBTemplate, DBParams


class WishCRUD(DBTemplate):
    def __init__(self):
        super().__init__(
            model_class=WishModel,
            schema_class=Wish,
            params=DBParams(
                exclude_fields_on_creation={'id'}
            )
        )
