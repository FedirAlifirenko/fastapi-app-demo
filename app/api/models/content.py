import base64
from typing import Any, ClassVar, Self

from pydantic import BaseModel, ConfigDict


class ContentCreate(BaseModel):
    protection_system_id: int
    encryption_key: str
    payload: str


class Content(BaseModel):
    id: int
    protection_system_id: int
    encryption_key: str
    encrypted_payload: str

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        **kwargs,
    ) -> Self:
        if isinstance(obj.encryption_key, bytes):
            obj.encryption_key = cls._to_base64(obj.encryption_key)

        if isinstance(obj.encrypted_payload, bytes):
            obj.encrypted_payload = cls._to_base64(obj.encrypted_payload)

        return super().model_validate(obj, **kwargs)

    @staticmethod
    def _to_base64(data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")


class DecryptedContent(BaseModel):
    payload: str
