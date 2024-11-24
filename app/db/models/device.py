from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class Device(BaseModel):
    __tablename__ = "devices"

    name: Mapped[str] = mapped_column(String(255))
    protection_system_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("protection_systems.id", ondelete="CASCADE")
    )

    protection_system = relationship("ProtectionSystem", back_populates="devices", lazy="selectin")
