from enum import StrEnum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import BaseModel


class EncryptionMode(StrEnum):
    aes_ecb: str = "AES_ECB"
    aes_cbc: str = "AES_CBC"


class ProtectionSystem(BaseModel):
    __tablename__ = "protection_systems"

    name: Mapped[str] = mapped_column(String(255))
    encryption_mode: Mapped[EncryptionMode] = mapped_column(Enum(EncryptionMode))

    devices = relationship(
        "Device", back_populates="protection_system", lazy="selectin", cascade="all,delete"
    )
    contents = relationship(
        "Content", back_populates="protection_system", lazy="selectin", cascade="all,delete"
    )
