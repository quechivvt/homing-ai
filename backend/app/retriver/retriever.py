from abc import ABC, abstractmethod
from app.models.knowledge_chunk import KnowledgeChunk


class Retriever(ABC):

    @abstractmethod
    async def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[KnowledgeChunk]:
        """
        Retrieve the most relevant knowledge chunks.
        """
        raise NotImplementedError