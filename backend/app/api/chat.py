from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.dependencies import get_chat_service
from fastapi.responses import StreamingResponse

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

@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    chat_service : ChatService = Depends(get_chat_service),
)->StreamingResponse:
    return await chat_service.stream(request=request)
    