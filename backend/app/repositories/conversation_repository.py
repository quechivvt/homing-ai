from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update

from app.models import Conversation
from app.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db):
        super().__init__(db, Conversation)

    async def create(
        self,
        title: str,
        session_id: str,
    ) -> Conversation:
        conversation = Conversation(
            title=title,
            session_id=session_id,
        )

        self.db.add(conversation)

        await self.db.commit()
        await self.db.refresh(conversation)

        return conversation

    async def get_by_id(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )

        return result.scalar_one_or_none()

    async def list_by_session(
        self,
        session_id: UUID,
    ) -> list[Conversation]:
        result = await self.db.execute(
            select(Conversation)
            .where(
                Conversation.session_id == session_id
            )
            .order_by(
                Conversation.updated_at.desc()
            )
        )

        return list(result.scalars().all())

    async def delete(
        self,
        conversation: Conversation,
    ) -> None:
        await self.db.delete(conversation)
        await self.db.commit()

    async def update(
        self,
        conversation: Conversation,
    ) -> Conversation:
    
        await self.db.commit()
        await self.db.refresh(conversation)
    
        return conversation

    async def touch(
        self,
        conversation_id: UUID,
    ) -> None:
        await self.db.execute(
            update(Conversation)
            .where(Conversation.id == conversation_id)
            .values(
                updated_at=datetime.now(UTC)
            )
        )

        await self.db.commit()