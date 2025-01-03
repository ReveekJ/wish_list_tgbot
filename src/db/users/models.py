from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db_connect import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)

    own_wish_lists: Mapped[Optional[list["WishListModel"]]] = relationship(
        back_populates="owner"
    )
    member_wish_lists: Mapped[Optional[list["WishListModel"]]] = relationship(
        secondary="wishlist_members",
        back_populates="members"
    )



from src.db.wish_lists.models import WishListModel
