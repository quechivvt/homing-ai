from typing import Literal

from pydantic import BaseModel

from app.schemas.message import PetCardContent
from app.schemas.pet import PetResponse


class BaseStreamEvent(BaseModel):
    event: str


class StatusEvent(BaseStreamEvent):
    event: Literal["status"] = "status"
    message: str


class TokenEvent(BaseStreamEvent):
    event: Literal["token"] = "token"
    token: str


class ToolStartEvent(BaseStreamEvent):
    event: Literal["tool_start"] = "tool_start"
    tool: str


class ToolEndEvent(BaseStreamEvent):
    event: Literal["tool_end"] = "tool_end"
    tool: str


class PetCardEvent(BaseStreamEvent):
    event: Literal["pet_card"] = "pet_card"
    pet: PetResponse


class ErrorEvent(BaseStreamEvent):
    event: Literal["error"] = "error"
    message: str


class DoneEvent(BaseStreamEvent):
    event: Literal["done"] = "done"