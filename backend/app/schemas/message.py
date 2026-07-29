from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.enum.message_role import MessageRole
from app.schemas.common import ORMModel
from uuid import UUID


class MessageBase(BaseModel):
    role: MessageRole
    content: str


class MessageCreate(MessageBase):
    conversation_id: UUID
    rawdata: dict[str, Any] | None = None


class MessageUpdate(BaseModel):
    content: str | None = None
    rawdata: dict[str, Any] | None = None


class MessageResponse(ORMModel):
    id: UUID

    conversation_id: UUID

    role: MessageRole
    content: str

    rawdata: dict[str, Any] | None

    created_at: datetime