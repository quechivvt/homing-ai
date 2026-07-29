from app.repositories.pet_repository import PetRepository
from app.repositories.knowlede_repository import KnowledgeRepository
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