from dataclasses import dataclass

from app.models.conversation import Conversation
from app.schemas.chat import ChatRequest
from app.schemas.chat import ChatResult
from app.schemas.message import MessageCreate
from typing import Any


@dataclass
class PipelineState:
    request: ChatRequest

    conversation: Conversation

    history: list

    chunks: list

    context: str

    prompt: Any | None = None

    result: ChatResult | None = None

    assistant_message: MessageCreate | None = None