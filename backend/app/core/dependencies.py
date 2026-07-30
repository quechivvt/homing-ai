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

def get_conversation_cache_repository():
    return ConversationCacheRepository(redis_client)

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

    

def get_embedding_Service():
    return EmbeddingService()

def get_conversation_service(
    message_repository = Depends(get_message_repository),
    conversation_repository = Depends(get_conversation_repository),
    conversation_cache_repository = Depends(get_conversation_cache_repository)
):
    return ConversationService(conversation_repository,message_repository,conversation_cache_repository)

#Retriver
def get_knowledge_retriever(
    knowledge_repository = Depends(get_knowledge_repository),
    embedding_service = Depends(get_embedding_Service),
    max_distance = settings.MAX_DISTANCE
):
    return KnowledgeRetriever(
        knowledge_repository=knowledge_repository,
        embedding_service=embedding_service,
        max_distance= max_distance)

def get_chat_result_mapper(
    pet_repository = Depends(get_pet_repository)    
):
    return ChatResultMapper(pet_repository=pet_repository)

def get_context_builder( ):
    return ContextBuilder()

def get_pipeline(
    history_manager = Depends(get_history_manager),
    conversation_manager = Depends(get_conversation_manager),
    knowledge_retriever = Depends(get_knowledge_retriever),
    chat_result_mapper = Depends(get_chat_result_mapper),
    context_builder = Depends(get_context_builder),
):
    if settings.PIPELINE =="LANGCHAIN":
        return LangChainPipeline(
            history_manager=history_manager,
            conversation_manager=conversation_manager,
            knowledge_retriever=knowledge_retriever,
            chat_result_mapper = chat_result_mapper,
            context_builder = context_builder
        )

#Service
def get_chat_service(
    pipeline = Depends(get_pipeline)
):
    return ChatService(pipeline=pipeline)