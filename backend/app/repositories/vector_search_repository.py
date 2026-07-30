from sqlalchemy.ext.asyncio import AsyncSession


class VectorSearchRepository:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def search_pets(
        self,
        embedding: list[float],
        limit: int = 5,
    ):
        """
        Semantic search for pets.

        TODO:
        - Join PetEmbedding with Pet.
        - Order by vector distance.
        - Filter unavailable pets.
        """
        raise NotImplementedError

    async def search_messages(
        self,
        embedding: list[float],
        conversation_id: int | None = None,
        limit: int = 5,
    ):
        """
        Semantic search for messages.

        TODO:
        - Join MessageEmbedding with Message.
        - Optionally filter by conversation.
        - Order by vector distance.
        """
        raise NotImplementedError