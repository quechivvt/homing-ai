from fastapi import APIRouter,Depends
from uuid import UUID
from app.schemas.conversation import ConversationUpdate
from app.schemas.conversation import (
    ConversationDetailResponse,
    ConversationResponse
)
from app.core.dependencies import get_conversation_service
from app.services.conversation_service import ConversationService

router = APIRouter(
    prefix="/v1/conversations",
    tags=["Conversation"]
)

@router.get("")
async def get_conversations_session(
    session_id:str,
    conversation_service : ConversationService = Depends(get_conversation_service),
)->list[ConversationResponse]:
    return await conversation_service.get_conversations(session_id=session_id)
    

@router.get("/{conversation_id}")
async def get_conversation_by_id(
    conversation_id: UUID,
    conversation_service :ConversationService = Depends(get_conversation_service),
)-> ConversationDetailResponse:
    return await conversation_service.get_conversation_by_id(conversation_id=conversation_id)

@router.patch("/{conversation_id}")
async def update_conversation(
    conversation_id: UUID,
    request: ConversationUpdate,
    conversation_service :ConversationService = Depends(get_conversation_service),
)->ConversationResponse:
    return await conversation_service.update_conversation(conversation_id=conversation_id,title=request.title)

@router.delete("/{conversation_id}")
async def delete_conversation_by_id(
    conversation_id: UUID,
    conversation_service :ConversationService = Depends(get_conversation_service),
):
    await conversation_service.delete_conversation(conversation_id=conversation_id)