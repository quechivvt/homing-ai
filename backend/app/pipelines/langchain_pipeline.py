from app.pipelines.pipeline import ChatPipeline
from app.schemas.chat import (
    ChatResponse,
    ChatMessage,
    ChatRequest
)
from langchain_core.messages import HumanMessage

from app.prompts.chat_prompt import chat_prompt
from app.pipelines.history_manager import HistoryManager
from app.pipelines.conversation_manager import ConversationManager
from app.schemas.message import MessageCreate, TextContent
from app.retriver.knowledge_retriever import KnowledgeRetriever
from app.mapper.chat_result_mapper import ChatResultMapper
from app.core.logging import logger
from app.pipelines.context_builder import ContextBuilder
from app.pipelines.pipeline_state import PipelineState
from app.models.chat_model import ChatModel
from app.schemas.stream_event import TokenEvent, ConversationEvent
from app.schemas.chat import ChatResult
from app.models.title_model import TitleModel


class LangChainPipeline(ChatPipeline):
    def __init__(
            self, 
            conversation_manager : ConversationManager,
            history_manager : HistoryManager,
            knowledge_retriever: KnowledgeRetriever,
            chat_result_mapper : ChatResultMapper,
            context_builder : ContextBuilder,
            chat_model: ChatModel,
            title_model: TitleModel,

        ):
            self.conversation_manager = conversation_manager
            self.history_manager = history_manager
            self.knowledge_retriever = knowledge_retriever
            self.chat_result_mapper = chat_result_mapper
            self.context_builder = context_builder
            self.chat_model = chat_model
            self.title_model = title_model

    async def prepare(self, request: ChatRequest) -> PipelineState:
        conversation = await self.conversation_manager.get_or_create(request)
        history = await self.history_manager.load(
            conversation.id
        )
        # ===== RAG DISABLED =====
        #chunks = await self.knowledge_retriever.retrieve(
        #    request.message
        #)
        #context = self.context_builder.build(chunks)

        return PipelineState(
            request=request,
            conversation=conversation,
            history=history,
            # RAG disabled
            chunks=[],
            context="",
        )

    async def build_prompt(self, state:PipelineState):
        state.prompt = await chat_prompt.ainvoke(
            {
                "history": state.history,
                "input": state.request.message,
                #"context": state.context,
            }
        )
        return state

    async def invoke(self, state:PipelineState):

        response = await self.chat_model.invoke(
            state.prompt.to_messages()
        )

        state.result = ChatResult(
            answer=response.text()
        )

        return state

    from langchain_core.messages import HumanMessage

    async def generate_title(
        self,
        state: PipelineState,
    ):
        if state.conversation.title != "New Chat":
            return

        user_messages = [
            message.content
            for message in state.history
            if isinstance(message, HumanMessage)
        ]

        user_messages.append(state.request.message)

        if len(user_messages) < 2:
            return

        conversation = "\n".join(
            f"User: {message}"
            for message in user_messages[-3:]
        )

        title = await self.title_model.generate(
            conversation=conversation,
        )

        await self.conversation_manager.update_title(
            conversation_id=state.conversation.id,
            session_id=state.conversation.session_id,
            title=title,
        )

    async def map_result(self, state:PipelineState):

        state.assistant_message = await self.chat_result_mapper.map(
            state.result
        )
        return state
        

    async def finalize(
        self,
        state: PipelineState,
    ) -> ChatResponse:

        await self.history_manager.save(
            conversation_id=state.conversation.id,
            messages=[
                MessageCreate(
                    role="user",
                    content=[
                        TextContent(
                            text=state.request.message
                        )
                    ],
                ),
                state.assistant_message,
            ],
        )

        await self.conversation_manager.touch(
            state.conversation.id
        )

        return ChatResponse(
            conversation_id=state.conversation.id,
            messages=[
                ChatMessage(
                    role=state.assistant_message.role,
                    content=state.assistant_message.content,
                )
            ],
        )

    async def run(self, request: ChatRequest):

        state = await self.prepare(request)

        state = await self.build_prompt(state)

        state = await self.invoke(state)

        state = await self.map_result(state)

        response = await self.finalize(state)
        
        await self.generate_title(state)
        
        return response

    async def stream(self, request: ChatRequest):
    
        state = await self.prepare(request)

        yield ConversationEvent(
            conversation_id=state.conversation.id,
        )
    
        state = await self.build_prompt(state)
    
        messages = state.prompt.to_messages()
    
        answer = []
        try:
    
            async for event in self.chat_model.stream(messages):
    
                if isinstance(event, TokenEvent):
                    answer.append(event.token)
    
                yield event
    
        except Exception:
            logger.exception("Streaming failed")
            raise
    
    
        state.result = ChatResult(
            answer="".join(answer)
        )
    
    
        await self.map_result(state)
    
        response = await self.finalize(state)
    
        await self.generate_title(state)