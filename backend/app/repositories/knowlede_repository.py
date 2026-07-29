from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge_chunk import KnowledgeChunk


class KnowledgeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def insert(
        self,
        chunk: KnowledgeChunk,
    ) -> None:
        """
        Add a knowledge chunk to the current transaction.
        """
        self.db.add(chunk)

    async def delete_by_source(
        self,
        source_type: str,
        source_id: UUID,
    ) -> None:
        """
        Delete all chunks belonging to a source object.
        Example:
            source_type = "pet"
            source_id = pet.id
        """
        stmt = (
            delete(KnowledgeChunk)
            .where(KnowledgeChunk.source_type == source_type)
            .where(KnowledgeChunk.source_id == source_id)
        )

        await self.db.execute(stmt)

    async def similarity_search(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[KnowledgeChunk]:
        """
        Return the most similar chunks using cosine distance.
        """
        stmt = (
            select(KnowledgeChunk)
            .order_by(
                KnowledgeChunk.embedding.cosine_distance(embedding)
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_source(
        self,
        source_type: str,
        source_id: UUID,
    ) -> list[KnowledgeChunk]:
        stmt = (
            select(KnowledgeChunk)
            .where(KnowledgeChunk.source_type == source_type)
            .where(KnowledgeChunk.source_id == source_id)
            .order_by(KnowledgeChunk.chunk_index)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()

    async def refresh(
        self,
        chunk: KnowledgeChunk,
    ) -> None:
        await self.db.refresh(chunk)

    async def flush(self) -> None:
        await self.db.flush()