from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.repositories.pet_repository import PetRepository
from app.services.crawl_service import CrawlService
from app.repositories.message_repository import MessageRepository
from app.repositories.conversation_repository import ConversationRepository

from app.core.config import settings
from app.pipelines.langchain_pipeline import LangChainPipeline
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService
from app.pipelines.history_manager import HistoryManager
from app.pipelines.conversation_manager import ConversationManager
from app.cache.history_cache_repository import HistoryCacheRepository
from app.cache.conversation_cache_repository import ConversationCacheRepository
from app.core.redis import redis_client
from app.cache.conversation_cache_repository import ConversationCacheRepository
from app.repositories.knowledge_repository import KnowledgeRepository
from app.retriver.knowledge_retriever import KnowledgeRetriever
from app.services.embedding_service import EmbeddingService
from app.mapper.chat_result_mapper import ChatResultMapper
from app.pipelines.context_builder import ContextBuilder
from app.chains.chatbot_chain import model
from app.models.langchain_chat_model import LangChainChatModel
from app.models.chat_model_provider import ChatModelProvider
from app.tools.find_pets_tool import FindPetsTool
from app.tools.get_pet_tool import GetPetTool
from app.tools.compare_pets_tool import ComparePetsTool
from app.tools.tool_registry import ToolRegistry
from app.tools.tool_executor import ToolExecutor
from app.models.title_model import TitleModel
from app.models.langchain_title_model import LangChainTitleModel

import langchain_openai.chat_models.base as base
from app.core.langchain_patch import _convert_message_to_dict

base._convert_message_to_dict = _convert_message_to_dict

#Repository

def get_pet_repository(
    db: AsyncSession = Depends(get_db),
):
    return PetRepository(db)

def get_message_repository(
    db: AsyncSession = Depends(get_db),
):
    return MessageRepository(db)


def get_conversation_repository(
    db: AsyncSession = Depends(get_db),
):
    return ConversationRepository(db)

def get_knowledge_repository(
    db: AsyncSession = Depends(get_db),
):
    return KnowledgeRepository(db)

#Service

def get_crawl_service(
    db: AsyncSession = Depends(get_db),
    pet_repository: PetRepository = Depends(get_pet_repository),
) -> CrawlService:
    return CrawlService(
        db=db,
        pet_repository=pet_repository,
    )


#def get_vector_search_repository(
#    db: AsyncSession = Depends(get_db),
#):
#    return VectorSearchRepository(db)

#Cache
def get_history_cache_repository():
    return HistoryCacheRepository(redis=redis_client)

def get_conversation_cache_repository():
    return ConversationCacheRepository(redis=redis_client)

# Manager
def get_history_manager(
    message_repository = Depends(get_message_repository),
    history_cache_repository = Depends(get_history_cache_repository)
):
    return HistoryManager(message_repository,history_cache_repository)

def get_conversation_manager(
    conversation_repository = Depends(get_conversation_repository),
    conversation_cache_repository = Depends(get_conversation_cache_repository),    
):
    return ConversationManager(conversation_repository, conversation_cache_repository)

# Embedding
async def get_embedding_service():
    return EmbeddingService()

def get_conversation_service(
    message_repository = Depends(get_message_repository),
    conversation_repository = Depends(get_conversation_repository),
    conversation_cache_repository = Depends(get_conversation_cache_repository)
):
    return ConversationService(conversation_repository,message_repository,conversation_cache_repository)

# Tool

def get_find_pets_tool(
    pet_repository: PetRepository = Depends(get_pet_repository),
):
    return FindPetsTool(
        repository=pet_repository,
    )


def get_get_pet_tool(
    pet_repository: PetRepository = Depends(get_pet_repository),
):
    return GetPetTool(
        repository=pet_repository,
    )


def get_compare_pets_tool(
    pet_repository: PetRepository = Depends(get_pet_repository),
):
    return ComparePetsTool(
        repository=pet_repository,
    )

def get_tool_registry(
    find_pets_tool: FindPetsTool = Depends(get_find_pets_tool),
    get_pet_tool: GetPetTool = Depends(get_get_pet_tool),
    compare_pets_tool: ComparePetsTool = Depends(get_compare_pets_tool),
):
    return ToolRegistry(
        find_pet=find_pets_tool,
        get_pet=get_pet_tool,
        compare_pet=compare_pets_tool,
    )

def get_tool_executor(
    tool_registry = Depends(get_tool_registry)
):
    return ToolExecutor(tool_registry)

#Retriver
def get_knowledge_retriever(
    knowledge_repository = Depends(get_knowledge_repository),
    embedding_service = Depends(get_embedding_service),
):
    return KnowledgeRetriever(
        knowledge_repository=knowledge_repository,
        embedding_service=embedding_service,
        max_distance= settings.MAX_DISTANCE)

def get_chat_result_mapper(
    pet_repository = Depends(get_pet_repository)    
):
    return ChatResultMapper(pet_repository=pet_repository)

def get_context_builder( ):
    return ContextBuilder()



# Model
def get_chat_model_provider(
    tool_registry: ToolRegistry = Depends(get_tool_registry),
) -> ChatModelProvider:

    return ChatModelProvider(
        model=model,
        tools=tool_registry.langchain(),
    )

def get_chat_model(
    provider = Depends(get_chat_model_provider),
    executor : ToolExecutor = Depends(get_tool_executor),
) -> LangChainChatModel:
    return LangChainChatModel(provider=provider,executor=executor)

def get_title_model(
    provider: ChatModelProvider = Depends(get_chat_model_provider),
) -> TitleModel:
    return LangChainTitleModel(
        provider=provider,
    )

def get_pipeline(
    history_manager = Depends(get_history_manager),
    conversation_manager = Depends(get_conversation_manager),
    knowledge_retriever = Depends(get_knowledge_retriever),
    chat_result_mapper = Depends(get_chat_result_mapper),
    context_builder = Depends(get_context_builder),
    chat_model = Depends(get_chat_model),
    title_model = Depends(get_title_model),
):
    if settings.PIPELINE =="LANGCHAIN":
        return LangChainPipeline(
            history_manager=history_manager,
            conversation_manager=conversation_manager,
            knowledge_retriever=knowledge_retriever,
            chat_result_mapper = chat_result_mapper,
            context_builder = context_builder,
            chat_model=chat_model,
            title_model=title_model
        )


#Service
def get_chat_service(
    pipeline = Depends(get_pipeline)
):
    return ChatService(pipeline=pipeline)