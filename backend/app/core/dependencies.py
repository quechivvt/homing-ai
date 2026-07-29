from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.repositories.pet_repository import PetRepository
from app.services.crawl_service import CrawlService
from app.repositories.message_repository import MessageRepository
from app.repositories.conversation_repository import ConversationRepository

from app.repositories.vector_search_repository import VectorSearchRepository
from app.core.config import settings
from app.pipelines.langchain_pipeline import LangChainPipeline
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService

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


def get_crawl_service(
    db: AsyncSession = Depends(get_db),
    pet_repository: PetRepository = Depends(get_pet_repository),
) -> CrawlService:
    return CrawlService(
        db=db,
        pet_repository=pet_repository,
    )


def get_vector_search_repository(
    db: AsyncSession = Depends(get_db),
):
    return VectorSearchRepository(db)

def get_pipeline(
    message_repository = Depends(get_message_repository),
    conversation_repository = Depends(get_conversation_repository),
):
    if settings.PIPELINE =="LANGCHAIN":
        return LangChainPipeline(
            message_repository,
            conversation_repository,
        )

def get_chat_service(
    pipeline = Depends(get_pipeline)
):
    return ChatService(pipeline=pipeline)

def get_conversation_service(
    message_repository = Depends(get_message_repository),
    conversation_repository = Depends(get_conversation_repository),
):
    return ConversationService(conversation_repository,message_repository)