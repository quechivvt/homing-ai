from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class Pet(Base):
    __tablename__ = "pets"

    __table_args__ = (
        UniqueConstraint(
            "source",
            "source_id",
            name="uq_pet_source_source_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    # ===== Source Information =====
    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    source_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    detail_url: Mapped[str | None] = mapped_column(Text)

    image_url: Mapped[str | None] = mapped_column(Text)

    # ===== Basic Information =====

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    species: Mapped[str | None] = mapped_column(String(50))

    breed: Mapped[str | None] = mapped_column(String(100))

    color: Mapped[str | None] = mapped_column(String(100))

    gender: Mapped[str | None] = mapped_column(String(30))

    age: Mapped[str | None] = mapped_column(String(50))

    weight: Mapped[str | None] = mapped_column(String(50))

    vaccination: Mapped[str | None] = mapped_column(String(100))

    chip: Mapped[str | None] = mapped_column(String(100))

    online_adoption_available: Mapped[bool | None] = mapped_column(Boolean)

    contact_adoption: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        comment="Description used for embedding generation",
    )

    # ===== Crawled Raw Data =====

    raw_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    # ===== Status =====

    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ===== Timestamp =====

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )