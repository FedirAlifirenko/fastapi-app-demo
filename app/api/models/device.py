from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class DeviceCreate(BaseModel):
    name: str
    protection_system_id: int


class Device(BaseModel):
    id: int
    name: str
    protection_system_id: int

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class DeviceUpdate(BaseModel):
    name: str | None = None
    protection_system_id: int | None = None
