from app.pipelines.pipeline import ChatPipeline
from app.schemas.chat import (
    ChatResponse,
    ChatMessage,
    ChatRequest
)
from app.chains.chatbot_chain import structured_model
from app.prompts.chat_prompt import chat_prompt
from app.pipelines.history_manager import HistoryManager
from app.pipelines.conversation_manager import ConversationManager
from app.schemas.message import MessageCreate, TextContent
from app.retriver.knowledge_retriever import KnowledgeRetriever
from app.mapper.chat_result_mapper import ChatResultMapper
from app.core.logging import logger
from app.pipelines.context_builder import ContextBuilder


class LangChainPipeline(ChatPipeline):
    def __init__(
            self, 
            conversation_manager : ConversationManager,
            history_manager : HistoryManager,
            knowledge_retriever: KnowledgeRetriever,
            chat_result_mapper : ChatResultMapper,
            context_builder : ContextBuilder,
        ):
            self.conversation_manager = conversation_manager
            self.history_manager = history_manager
            self.knowledge_retriever = knowledge_retriever
            self.chat_result_mapper = chat_result_mapper
            self.context_builder = context_builder

    async def run(self, request: ChatRequest):
        conversation = await self.conversation_manager.get_or_create(request=request)
        
        history_messages = await self.history_manager.load(conversation_id=conversation.id)

        # Retriever
        chunks = await self.knowledge_retriever.retrieve(
            request.message
        )

        # Context Builder
        context = self.context_builder.build(chunks)

        logger.info(f"CONTEXT: {context}")

        prompt = await chat_prompt.ainvoke(
            {
                "history": history_messages,
                "input": request.message,
                "context": context,
            }
        )

        result = await structured_model.ainvoke(prompt)
        logger.info(f"RESULT: {result}")
        
        assistant_message = await self.chat_result_mapper.map(
            result
        )
        #answer ="hihihi" 

        await self.history_manager.save(
            conversation_id=conversation.id,
            messages=[
                MessageCreate(
                    role="user",
                    content=[
                        TextContent(
                            text=request.message,
                        )
                    ],
                ),
                assistant_message,
            ],
        )

        await self.conversation_manager.touch(
            conversation.id
        )
    
        return ChatResponse(
            conversation_id=conversation.id,
            messages=[
                ChatMessage(
                    role=assistant_message.role,
                    content=assistant_message.content,
                )
            ],
        )