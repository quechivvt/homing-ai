# app/chains/chat_model.py

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.schemas.chat import ChatResult
from app.schemas.stream_event import BaseStreamEvent


class ChatModel(ABC):

    @abstractmethod
    async def invoke(self, prompt) -> ChatResult:
        ...

    @abstractmethod
    async def stream(self, prompt) -> AsyncIterator[BaseStreamEvent]:
        ...