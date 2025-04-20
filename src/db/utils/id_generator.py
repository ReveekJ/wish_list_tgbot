from sqlalchemy import select

from src.db.db_connect import get_session


class IdGenerator:
    @classmethod
    def __execute_query(cls, query):
        with get_session() as session:
            return session.execute(query).scalars().first()

    @classmethod
    def generate_wish_list_id(cls):
        from src.db.wish_lists.models import WishListModel

        query = select(WishListModel.id).order_by(WishListModel.id.desc())
        return cls.__execute_query(query) + 1

    @classmethod
    def generate_wish_id(cls):
        from src.db.wishes.models import WishModel

        query = select(WishModel.id).order_by(WishModel.id.desc())
        return cls.__execute_query(query) + 1
