from app.retriver.retriever import Retriever
from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.embedding_service import EmbeddingService
from app.models.knowledge_chunk import KnowledgeChunk


class KnowledgeRetriever(Retriever):

    DEFAULT_K = 5

    def __init__(
        self,
        knowledge_repository : KnowledgeRepository,
        embedding_service : EmbeddingService,
        max_distance : float = 0.4,
    ):
        self.knowledge_repository = knowledge_repository
        self.embedding_service = embedding_service
        self.max_distance = max_distance

    async def retrieve(
        self,
        query: str,
        k: int = DEFAULT_K,
    ) -> list[KnowledgeChunk]:
        """
        Retrieve the most relevant knowledge chunks for a user query.
        """

        embedding = await self.embedding_service.embed_query(
            query
        )

        chunks = await self.knowledge_repository.search(
            embedding=embedding,
            limit=k,
            max_distance=self.max_distance,
        )

        return chunks