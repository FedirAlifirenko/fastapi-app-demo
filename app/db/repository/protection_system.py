from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ProtectionSystem
from app.db.repository.base import SqlAlchemyRepository


class ProtectionSystemRepository(SqlAlchemyRepository[ProtectionSystem]):

    def __init__(self, *, db_session: AsyncSession):
        super().__init__(model=ProtectionSystem, db_session=db_session)
