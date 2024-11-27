from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel
from app.db.models.user_device import user_device

if TYPE_CHECKING:
    from app.db.models.device import Device

USERNAME_MAX_LENGTH = 10


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(length=USERNAME_MAX_LENGTH))
    devices: Mapped[list["Device"]] = relationship(secondary=user_device, back_populates="users")
