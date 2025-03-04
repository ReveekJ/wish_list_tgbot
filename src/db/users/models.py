import datetime
from typing import Optional, List

from sqlalchemy import BigInteger, Enum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db_connect import Base
from src.db.users.enums import GenderEnum


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True)
    birthdate: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    gender: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum), nullable=True)
    name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    language_code: Mapped[str]
    is_blocked: Mapped[bool]

    own_wish_lists: Mapped[Optional[list["WishListModel"]]] = relationship(
        back_populates="owner"
    )
    member_wish_lists: Mapped[Optional[list["WishListModel"]]] = relationship(
        secondary="wishlist_members",
        back_populates="members"
    )
    booked_wishes: Mapped[Optional[List["WishModel"]]] = relationship(
        back_populates='booked_by_user'
    )


from src.db.wish_lists.models import WishListModel
from src.db.wishes.models import WishModel
