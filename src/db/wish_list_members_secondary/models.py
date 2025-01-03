from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.db_connect import Base


class WishListMembersModel(Base):
    __tablename__ = "wishlist_members"

    user_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("users.id"), primary_key=True)
    wishlist_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("wish_lists.id"), primary_key=True)
