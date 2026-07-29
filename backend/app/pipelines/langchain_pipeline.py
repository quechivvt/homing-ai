from app.pipelines.pipeline import ChatPipeline
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.chat import ChatRequest, ChatResponse
from langchain_core.messages import AIMessage, HumanMessage
from app.core.logging import logger
from app.schemas.chat import (
    ChatResponse,
    TextMessage,
)
from app.chains.chatbot_chain import chat_chain
from app.mapper.message_mapper import MessageMapper

class LangChainPipeline(ChatPipeline):
    def __init__(
            self, 
            message_repository : MessageRepository,
            conversation_repository : ConversationRepository,
        ):
            self.conversation_repository = conversation_repository
            self.message_repository = message_repository

    async def run(self, request: ChatRequest):
        if request.conversation_id is None:
            conversation = await self.conversation_repository.create(
                    title=request.message,
                    session_id=request.session_id
                )
        else:
            conversation = await self.conversation_repository.get_by_id(
                request.conversation_id                )
        
        history = await self.message_repository.get_by_conversation(conversation.id)

        history_messages = []

        for message in history:
            if message.role == "user":
                history_messages.append(
                    HumanMessage(content=message.content)
                )
            else:
                history_messages.append(
                    AIMessage(content=message.content)
                )

        answer = await chat_chain.ainvoke(
            {
                "history": history_messages,
                "input": request.message,
            }
        )

        await self.message_repository.create(
            conversation_id=conversation.id,
            role="user",
            content=request.message,
        )

        await self.message_repository.create(
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
        )
    
        return ChatResponse(
            conversation_id=conversation.id,
            messages=[
                TextMessage(content=answer,role="assistant"),
            ],
        )