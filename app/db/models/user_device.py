from sqlalchemy import Column, ForeignKey, Table

from app.db.models.base import BaseModel

user_device = Table(
    "user_device",
    BaseModel.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("device_id", ForeignKey("devices.id")),
)
