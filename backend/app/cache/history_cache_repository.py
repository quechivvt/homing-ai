from uuid import UUID

from pydantic import BaseModel

from app.cache.cache_keys import CacheKey
from app.cache.cache_repository import CacheRepository
from app.schemas.message import MessageCreate

class ConversationHistoryCache(BaseModel):
    messages: list[MessageCreate]


class HistoryCacheRepository(CacheRepository):

    DEFAULT_TTL = 60 * 30  # 30 minutes

    async def get_history(
        self,
        conversation_id: UUID,
    ) -> ConversationHistoryCache | None:

        return await self.get(
            key=CacheKey.conversation_history(conversation_id),
            model=ConversationHistoryCache,
        )

    async def set_history(
        self,
        conversation_id: UUID,
        messages: list[MessageCreate],
    ) -> None:

        await self.set(
            key=CacheKey.conversation_history(conversation_id),
            value=ConversationHistoryCache(messages=messages),
            ttl=self.DEFAULT_TTL,
        )

    async def delete_history(
        self,
        conversation_id: UUID,
    ) -> None:

        await self.delete(
            CacheKey.conversation_history(conversation_id),
        )