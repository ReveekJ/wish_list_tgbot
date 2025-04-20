from typing import Optional

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.db.db_connect import Base
from src.db.utils.id_generator import IdGenerator


class WishListModel(Base):
    __tablename__ = "wish_lists"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, insert_default=IdGenerator.generate_wish_list_id)
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
