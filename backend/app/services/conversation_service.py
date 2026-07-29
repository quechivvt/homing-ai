from fastapi import HTTPException,status

from app.schemas.conversation import (   
    ConversationDetailResponse, 
    ConversationResponse
)
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from uuid import UUID
from app.mapper.message_mapper import MessageMapper
from app.exceptions.not_found_exception import NotFoundException

class ConversationService:
    def __init__(
        self,
        conversation_repository : ConversationRepository,
        message_repository : MessageRepository
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    async def get_conversations(
        self,
        session_id: str,
    ) -> list[ConversationResponse]:

        conversations = await self.conversation_repository.list_by_session(
            session_id
        )

        return [
            ConversationResponse(
                id=conversation.id,
                title=conversation.title,
                session_id = conversation.session_id,
                created_at=conversation.created_at,
                updated_at=conversation.updated_at,
            )
            for conversation in conversations
        ]

    async def get_conversation_by_id(self, conversation_id:UUID):
        conversation = await self.conversation_repository.get_by_id(conversation_id=conversation_id)

        if conversation is None:
            raise NotFoundException("Conversation")

        messages = await self.message_repository.get_by_conversation(conversation_id=conversation_id)
        return ConversationDetailResponse(
            id = conversation_id,
            title= conversation.title,
            updated_at=conversation.updated_at,
            created_at=conversation.created_at,
            messages=[
                MessageMapper.to_chat_message(message)
                for message in messages
            ]
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

        await self.conversation_repository.delete(
            conversation
        )
