import asyncio

from app.core.database import AsyncSessionLocal
from app.repositories.pet_repository import PetRepository
from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService


async def main():
    async with AsyncSessionLocal() as db:

        pet_repository = PetRepository(db)
        knowledge_repository = KnowledgeRepository(db)
        embedding_service = EmbeddingService()

        ingestion_service = IngestionService(
            pet_repository=pet_repository,
            knowledge_repository=knowledge_repository,
            embedding_service=embedding_service,
        )


        chunks = await ingestion_service.ingest_pets()


if __name__ == "__main__":
    asyncio.run(main())