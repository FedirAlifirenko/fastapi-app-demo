from sqlalchemy import ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class Content(BaseModel):
    __tablename__ = "contents"

    protection_system_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("protection_systems.id", ondelete="CASCADE")
    )
    symmetric_key: Mapped[str] = mapped_column(String(255))
    payload: Mapped[bytes] = mapped_column(LargeBinary)

    protection_system = relationship("ProtectionSystem", back_populates="contents", lazy="selectin")
