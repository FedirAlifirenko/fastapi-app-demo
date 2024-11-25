from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Device
from app.db.repository.base import SqlAlchemyRepository


class DeviceRepository(SqlAlchemyRepository[Device]):

    def __init__(self, *, db_session: AsyncSession):
        super().__init__(model=Device, db_session=db_session)
