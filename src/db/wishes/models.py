from typing import Optional

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db_connect import Base
from src.db.utils.id_generator import IdGenerator


class WishModel(Base):
    __tablename__ = "wishes"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, insert_default=IdGenerator.generate_wish_id)
    wish_list_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("wish_lists.id"))

    name: Mapped[str]
    description: Mapped[Optional[str]]
    link_to_marketplace: Mapped[Optional[str]]
    price: Mapped[Optional[str]]
    photo: Mapped[Optional[str]]
    is_booked: Mapped[bool] = mapped_column(default=False)
    booked_by_user_id: Mapped[Optional[BigInteger]] = mapped_column(BigInteger, ForeignKey("users.id"))

    booked_by_user: Mapped[Optional["UserModel"]] = relationship(
        back_populates='booked_wishes'
    )
    wish_list: Mapped["WishListModel"] = relationship(
        back_populates="wishes"
    )


from src.db.users.models import UserModel
from src.db.wish_lists.models import WishListModel
