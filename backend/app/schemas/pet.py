from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.schemas.common import ORMModel


class PetBase(BaseModel):
    source: str
    source_id: str

    detail_url: str | None = None
    image_url: str | None = None

    name: str

    species: str | None = None
    breed: str | None = None
    color: str | None = None
    gender: str | None = None
    age: str | None = None
    weight: str | None = None

    vaccination: str | None = None
    chip: str | None = None

    online_adoption_available: bool | None = None
    contact_adoption: str | None = None

    description: str | None = None


class PetCreate(PetBase):
    raw_data: dict[str, Any]


class PetUpdate(BaseModel):
    detail_url: str | None = None
    image_url: str | None = None

    name: str | None = None
    species: str | None = None
    breed: str | None = None
    color: str | None = None
    gender: str | None = None
    age: str | None = None
    weight: str | None = None

    vaccination: str | None = None
    chip: str | None = None

    online_adoption_available: bool | None = None
    contact_adoption: str | None = None

    description: str | None = None

    raw_data: dict[str, Any] | None = None

    available: bool | None = None


class PetResponse(ORMModel):
    id: int

    source: str
    source_id: str

    detail_url: str | None
    image_url: str | None

    name: str

    species: str | None
    breed: str | None
    color: str | None
    gender: str | None
    age: str | None
    weight: str | None

    vaccination: str | None
    chip: str | None

    online_adoption_available: bool | None

    contact_adoption: str | None

    description: str | None

    available: bool

    created_at: datetime
    updated_at: datetime