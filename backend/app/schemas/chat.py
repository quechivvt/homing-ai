from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

from app.enum.message_role import MessageRole
from app.schemas.message import MessageContent


class ChatMessage(BaseModel):
    role: MessageRole
    content: list[MessageContent]


class ChatRequest(BaseModel):
    session_id: UUID | None = None
    conversation_id: UUID | None = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: UUID
    messages: list[ChatMessage]

class ChatResult(BaseModel):
    """
    Structured output returned by the LLM.
    This model is internal and will be mapped to MessageContent.
    """

    answer: str = Field(
        description="Natural language response for the user."
    )

    recommended_pet_ids: list[int] = Field(
        default_factory=list,
        description=(
            "IDs of pets that should be displayed as pet cards. "
            "Leave empty if no pet should be recommended."
        ),
    )
    