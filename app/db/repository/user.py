from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.repository.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):

    def __init__(self, *, db_session: AsyncSession):
        super().__init__(model=User, db_session=db_session)
