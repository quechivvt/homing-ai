from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from app.core.database import Base

from app.enum.message_role import MessageRole
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from app.enum.message_type import MessageType


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    role: Mapped[MessageRole] = mapped_column(
        Enum(MessageRole),
    )

    content: Mapped[list] = mapped_column(JSONB)

    message_type : Mapped[MessageType] = mapped_column(
        Enum(MessageType),
        default=MessageType.TEXT,
    )

    rawdata: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )