from typing import Generic, TypeVar

from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(
        self,
        db: AsyncSession,
        model: type[T],
    ):
        self.db = db
        self.model = model

    async def get_by_id(
        self,
        entity_id: int,
    ) -> T | None:
        result = await self.db.execute(
            select(self.model).where(
                self.model.id == entity_id
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
    ) -> list[T]:
        result = await self.db.execute(
            select(self.model)
        )

        return list(result.scalars().all())

    async def add(
        self,
        entity: T,
    ) -> T:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def add_all(
        self,
        entities: list[T],
    ) -> list[T]:
        self.db.add_all(entities)
        await self.db.flush()
        return entities

    async def delete(
        self,
        entity: T,
    ) -> None:
        await self.db.delete(entity)

    async def delete_by_id(
        self,
        entity_id: int,
    ) -> bool:
        result = await self.db.execute(
            delete(self.model).where(
                self.model.id == entity_id
            )
        )

        return result.rowcount > 0

    async def exists(
        self,
        entity_id: int,
    ) -> bool:
        result = await self.db.execute(
            select(
                exists().where(
                    self.model.id == entity_id
                )
            )
        )

        return bool(result.scalar())

    async def flush(
        self,
        entity: T,
    ) -> T:
        await self.db.flush()
        await self.db.refresh(entity)
        return entity