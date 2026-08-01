from app.repositories.conversation_repository import ConversationRepository
from app.models.conversation import Conversation
from app.cache.conversation_cache_repository import ConversationCacheRepository

from app.schemas.chat import ChatRequest
from uuid import UUID

class ConversationManager:
    def __init__(
        self, 
        conversation_repository: ConversationRepository,
        conversation_cache_repository :ConversationCacheRepository,
    ):
        self.conversation_repository = conversation_repository
        self.conversation_cache_repository = conversation_cache_repository

    async def get_or_create(self,request:ChatRequest)-> Conversation:
        if request.conversation_id is None:
            conversation = await self.conversation_repository.create(
                title="New Chat",
                session_id=str(request.session_id)
                )
            await self.conversation_cache_repository.delete_conversations(request.session_id)
        else:
            conversation = await self.conversation_repository.get_by_id(
            request.conversation_id
            )
            if conversation is None:
                conversation = await self.conversation_repository.create(
                    title=request.message,
                    session_id=str(request.session_id)
                )
                await self.conversation_cache_repository.delete_conversations(request.session_id)

        return conversation

    async def touch(
        self,
        conversation_id: UUID,
    ) -> None:
        await self.conversation_repository.touch(conversation_id)

    async def update_title(
        self,
        conversation_id: UUID,
        session_id: str,
        title: str,
    ):

        await self.conversation_repository.update_title(
            conversation_id=conversation_id,
            title=title,
        )

        await self.conversation_cache_repository.delete_conversations(
            session_id=session_id,
        )
        

    