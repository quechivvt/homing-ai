from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.schemas.common import ORMModel
from app.schemas.chat import ChatMessage

class ConversationBase(BaseModel):
    session_id: str
    title: str | None = None

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: str | None = None

class ConversationResponse(ORMModel):
    id: UUID
    session_id: str
    title: str | None
    created_at: datetime
    updated_at: datetime

class ConversationDetailResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[ChatMessage]