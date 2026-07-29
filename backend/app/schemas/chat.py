from typing import Literal, Union
from uuid import UUID

from pydantic import BaseModel


class TextMessage(BaseModel):
    type: Literal["text"] = "text"
    role: Literal["user","assistant"]
    content: str


class PetCardMessage(BaseModel):
    type: Literal["pet_card"] = "pet_card"
    pet_id: UUID
    name: str
    image_url: str
    gender: str
    age: str
    breed: str | None = None


ChatMessage = Union[
    TextMessage,
    PetCardMessage,
]


class ChatRequest(BaseModel):
    session_id: UUID | None = None
    conversation_id: UUID | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: UUID
    messages: list[ChatMessage]