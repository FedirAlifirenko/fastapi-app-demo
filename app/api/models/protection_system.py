from enum import StrEnum
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class EncryptionMode(StrEnum):
    aes_ecb: str = "AES_ECB"
    aes_cbc: str = "AES_CBC"


class ProtectionSystem(BaseModel):
    id: int
    name: str
    encryption_mode: EncryptionMode

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class ProtectionSystemCreate(BaseModel):
    name: str
    encryption_mode: EncryptionMode


class ProtectionSystemUpdate(BaseModel):
    name: str | None = None
    encryption_mode: EncryptionMode | None = None
