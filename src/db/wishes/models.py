from typing import Optional

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.db_connect import Base


class WishModel(Base):
    __tablename__ = "wishes"

    id: Mapped[BigInteger] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    wish_list_id: Mapped[BigInteger] = mapped_column(BigInteger, ForeignKey("wish_lists.id"))

    name: Mapped[str]
    description: Mapped[Optional[str]]
    link_to_marketplace: Mapped[Optional[str]]
    price: Mapped[Optional[str]]
    photo: Mapped[Optional[str]]
    # TODO: поле забронировано_пользователем

    wish_list: Mapped["WishListModel"] = relationship(
        back_populates="wishes"
    )


from src.db.users.models import UserModel
from src.db.wish_lists.models import WishListModel
