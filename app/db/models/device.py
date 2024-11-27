from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel
from app.db.models.user_device import user_device


class Device(BaseModel):
    __tablename__ = "devices"

    name: Mapped[str] = mapped_column(String(255))
    protection_system_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("protection_systems.id", ondelete="CASCADE")
    )

    protection_system = relationship("ProtectionSystem", back_populates="devices", lazy="selectin")
    users: Mapped[list["User"]] = relationship(secondary=user_device, back_populates="devices")  # noqa # type: ignore
