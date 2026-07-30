from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.dependencies import get_chat_service

router = APIRouter(
    prefix ="/v1",
    tags =["chat"]
)

@router.post("/chat")
async def chat(
    request: ChatRequest,
    chat_service : ChatService = Depends(get_chat_service)
)-> ChatResponse:
    return await chat_service.chat(request=request)
    
    