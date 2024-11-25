from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Content
from app.db.repository.base import SqlAlchemyRepository


class ContentRepository(SqlAlchemyRepository[Content]):

    def __init__(self, *, db_session: AsyncSession):
        super().__init__(model=Content, db_session=db_session)
