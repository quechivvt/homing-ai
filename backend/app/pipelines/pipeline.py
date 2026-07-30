from abc import ABC, abstractmethod

from app.schemas.chat import ChatRequest, ChatResponse


class ChatPipeline(ABC):

    @abstractmethod
    async def run(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        pass