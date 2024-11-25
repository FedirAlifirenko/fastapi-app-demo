from enum import StrEnum
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field


class EncryptionMode(StrEnum):
    aes_cbc: str = "AES_CBC"


class ProtectionSystem(BaseModel):
    id: int
    name: str
    encryption_mode: EncryptionMode

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class ProtectionSystemCreate(BaseModel):
    name: str = Field(..., examples=["My Protection System"])
    encryption_mode: EncryptionMode = Field(..., examples=[EncryptionMode.aes_cbc])


class ProtectionSystemUpdate(BaseModel):
    name: str | None = None
    encryption_mode: EncryptionMode | None = None
