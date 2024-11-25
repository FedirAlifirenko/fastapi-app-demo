from sqlalchemy import ForeignKey, Integer, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class Content(BaseModel):
    __tablename__ = "contents"

    protection_system_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("protection_systems.id", ondelete="CASCADE")
    )
    encryption_key: Mapped[bytes] = mapped_column(LargeBinary)
    encrypted_payload: Mapped[bytes] = mapped_column(LargeBinary)

    protection_system = relationship("ProtectionSystem", back_populates="contents", lazy="selectin")
