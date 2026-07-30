from pydantic import BaseModel

from app.cache.cache_keys import CacheKey
from app.cache.cache_repository import CacheRepository
from app.schemas.conversation import ConversationResponse


class ConversationListCache(BaseModel):
    conversations: list[ConversationResponse]


class ConversationCacheRepository(CacheRepository):

    DEFAULT_TTL = 60 * 30  # 30 minutes

    async def get_conversations(
        self,
        session_id: str,
    ) -> ConversationListCache | None:

        return await self.get(
            key=CacheKey.conversation_list(session_id),
            model=ConversationListCache,
        )

    async def set_conversations(
        self,
        session_id: str,
        conversations: list[ConversationResponse],
    ) -> None:

        await self.set(
            key=CacheKey.conversation_list(session_id),
            value=ConversationListCache(
                conversations=conversations,
            ),
            ttl=self.DEFAULT_TTL,
        )

    async def delete_conversations(
        self,
        session_id: str,
    ) -> None:

        await self.delete(
            CacheKey.conversation_list(session_id),
        )