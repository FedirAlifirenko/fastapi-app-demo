from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class SqlAlchemyRepository(Generic[ModelType]):

    def __init__(self, *, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

        self.pk_columns = [column for column in model.__table__.primary_key]

    async def create(self, commit: bool = True, **kwargs: Any) -> ModelType:
        instance = self.model(**kwargs)
        self.db_session.add(instance)
        if commit:
            await self.db_session.commit()
            await self.db_session.refresh(instance)
        return instance

    async def get(
        self, instance_pk: Any | tuple[Any, ...], with_for_update: bool = False
    ) -> ModelType | None:
        return await self.db_session.get(
            self.model,
            ident=instance_pk,
            populate_existing=True,
            with_for_update=with_for_update,
        )

    async def list(self, *where_criteria: Any, order_by: list[Any] | None = None) -> list[ModelType]:
        stmt = select(self.model)
        if where_criteria:
            stmt = stmt.where(*where_criteria)
        if order_by:
            stmt = stmt.order_by(*order_by)
        res = await self.db_session.execute(stmt)
        return [obj for obj in res.scalars()]

    async def update(self, instance: ModelType, commit: bool = True, **kwargs: Any) -> ModelType:
        for attr, value in kwargs.items():
            setattr(instance, attr, value)
        if commit:
            await self.db_session.commit()
            await self.db_session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType, commit: bool = True) -> None:
        await self.db_session.delete(instance)
        if commit:
            await self.db_session.commit()
