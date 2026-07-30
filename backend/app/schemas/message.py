from datetime import datetime
from typing import Any, Literal, Union

from pydantic import BaseModel

from app.enum.message_role import MessageRole
from app.schemas.common import ORMModel
from uuid import UUID

class TextContent(BaseModel):
    type: Literal["text"] = "text"
    text: str

class PetCardContent(BaseModel):
    type: Literal["pet_card"] = "pet_card"
    pet_id: int
    name: str
    image_url: str | None = None

MessageContent = Union[
    TextContent,
    PetCardContent,
]

class MessageBase(BaseModel):
    role: MessageRole
    content: str

class MessageCreate(BaseModel):
    role: MessageRole
    content: list[MessageContent]


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

