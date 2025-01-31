from typing import List

from sqlalchemy import select

from src.db.users.models import UserModel
from src.db.users.schemas import User
from src.db.wish_lists.schemas import WishList
from src.utils.db_template import DBTemplate


class UserCRUD(DBTemplate[UserModel, User]):
    def __init__(self):
        super().__init__(
            model_class=UserModel,
            schema_class=User,
        )

    def get_friends_of_user(self, user_id: int) -> List[User]:
        query = select(self._model_class).where(self._model_class.id == user_id)
        res = self._db.execute(query).scalars().first()
        wish_lists = [WishList.model_validate(i, from_attributes=True) for i in res.member_wish_lists]

        # достаем только уникальных юзеров
        unique_owner_ids = set()
        for w in wish_lists:
            unique_owner_ids.add(w.owner_id)

        return sorted([self.get_obj_by_id(i) for i in unique_owner_ids], key=lambda i: i.name)
