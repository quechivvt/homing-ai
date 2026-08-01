from app.builders.document_builder import DocumentBuilder
from app.models.knowledge_chunk import KnowledgeChunk
from app.repositories.knowledge_repository import KnowledgeRepository
from app.repositories.pet_repository import PetRepository
from app.services.embedding_service import EmbeddingService


class IngestionService:

    def __init__(
        self,
        pet_repository: PetRepository,
        knowledge_repository: KnowledgeRepository,
        embedding_service: EmbeddingService,
    ):
        self.pet_repository = pet_repository
        self.knowledge_repository = knowledge_repository
        self.embedding_service = embedding_service

    async def ingest_pets(self) -> list[KnowledgeChunk]:

        pets = await self.pet_repository.list_available()

        dogs = [p for p in pets if p.species.lower() == "dog"][:30]
        cats = [p for p in pets if p.species.lower() == "cat"][:30]

        pets = dogs + cats

        if not pets:
            return []

        documents = [
            DocumentBuilder.build_pet(pet)
            for pet in pets
        ]

        embeddings = await self.embedding_service.embed_documents(
            documents
        )

        chunks: list[KnowledgeChunk] = []

        try:

            for pet, document, embedding in zip(
                pets,
                documents,
                embeddings,
            ):

                await self.knowledge_repository.delete_by_source(
                    source_type="pet",
                    source_id=pet.id,
                )

                chunk = KnowledgeChunk(
                    source_type="pet",
                    source_id=pet.id,
                    chunk_index=0,
                    content=document,
                    embedding=embedding,
                    rawdata={
                        "pet_id": str(pet.id),
                        "name": pet.name,
                        "species": pet.species,
                        "breed": pet.breed,
                        "gender": pet.gender,
                        "source": pet.source,
                        "source_pet_id": pet.source_id,
                        "detail_url": pet.detail_url,
                        "image_url": pet.image_url,
                        "available": pet.available,
                        "raw_info": pet.raw_data,
                    },
                )

                await self.knowledge_repository.insert(chunk)

                chunks.append(chunk)

            await self.knowledge_repository.commit()

            for chunk in chunks:
                await self.knowledge_repository.refresh(chunk)

            return chunks

        except Exception:
            await self.knowledge_repository.rollback()
            raise