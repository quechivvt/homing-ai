from uuid import UUID

from app.exceptions.not_found_exception import NotFoundException
from app.mapper.message_mapper import MessageMapper
from app.cache.conversation_cache_repository import (
    ConversationCacheRepository,
)
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.conversation import (
    ConversationDetailResponse,
    ConversationResponse,
)


class ConversationService:

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        conversation_cache_repository: ConversationCacheRepository,
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.conversation_cache_repository = conversation_cache_repository

    async def get_conversations(
        self,
        session_id: str,
    ) -> list[ConversationResponse]:

        cached = await self.conversation_cache_repository.get_conversations(
            session_id
        )

        if cached:
            return cached.conversations

        conversations = await self.conversation_repository.list_by_session(
            session_id
        )

        responses = [
            ConversationResponse(
                id=conversation.id,
                title=conversation.title,
                session_id=conversation.session_id,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
            )
            for conversation in conversations
        ]

        await self.conversation_cache_repository.set_conversations(
            session_id=session_id,
            conversations=responses,
        )

        return responses

    async def get_conversation_by_id(
        self,
        conversation_id: UUID,
    ) -> ConversationDetailResponse:

        conversation = await self.conversation_repository.get_by_id(
            conversation_id=conversation_id
        )

        if conversation is None:
            raise NotFoundException("Conversation")

        messages = await self.message_repository.get_by_conversation(
            conversation_id=conversation_id
        )

        return ConversationDetailResponse(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[
                MessageMapper.to_chat_message(message)
                for message in messages
            ],
        )

    async def update_conversation(
        self,
        conversation_id: UUID,
        title: str,
    ) -> ConversationResponse:

        conversation = await self.conversation_repository.get_by_id(
            conversation_id
        )

        if conversation is None:
            raise NotFoundException("Conversation")

        conversation.title = title

        conversation = await self.conversation_repository.update(
            conversation
        )

        await self.conversation_cache_repository.delete_conversations(
            conversation.session_id
        )

        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            session_id=conversation.session_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )

    async def delete_conversation(
        self,
        conversation_id: UUID,
    ) -> None:

        conversation = await self.conversation_repository.get_by_id(
            conversation_id
        )

        if conversation is None:
            raise NotFoundException("Conversation")

        session_id = conversation.session_id

        await self.conversation_repository.delete(
            conversation
        )

        await self.conversation_cache_repository.delete_conversations(
            session_id
        )