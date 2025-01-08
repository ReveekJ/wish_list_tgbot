from typing import Optional

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.db_connect import Base


class WishListModel(Base):
    __tablename__ = "wish_lists"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    owner_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("users.id"))
    name: Mapped[str]

    owner: Mapped["UserModel"] = relationship(
        back_populates='own_wish_lists'
    )
    members: Mapped[Optional[list["UserModel"]]] = relationship(
        secondary="wishlist_members",
        back_populates="member_wish_lists"
    )
    wishes: Mapped[Optional[list["WishModel"]]] = relationship(
        back_populates="wish_list"
    )


from src.db.wishes.models import WishModel
from src.db.users.models import UserModel
