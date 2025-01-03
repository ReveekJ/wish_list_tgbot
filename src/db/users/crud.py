from src.db.users.models import UserModel
from src.db.users.schemas import User
from src.utils.db_template import DBTemplate, DBParams


class UserCRUD(DBTemplate):
    def __init__(self):
        super().__init__(
            model_class=UserModel,
            schema_class=User,
        )
