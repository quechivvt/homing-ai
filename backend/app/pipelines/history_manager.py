from uuid import UUID

from langchain_core.messages import AIMessage, HumanMessage
from pydantic import TypeAdapter

from app.cache.history_cache_repository import HistoryCacheRepository
from app.models.message import Message
from app.repositories.message_repository import MessageRepository
from app.schemas.message import (
    MessageContent,
    MessageCreate,
    PetCardContent,
    TextContent,
)


_MESSAGE_CONTENT_ADAPTER = TypeAdapter(list[MessageContent])


class HistoryManager:
    def __init__(
        self,
        message_repository: MessageRepository,
        history_cache_repository: HistoryCacheRepository,
    ):
        self.message_repository = message_repository
        self.history_cache_repository = history_cache_repository

    def _to_message_create(
        self,
        message: Message,
    ) -> MessageCreate:
        return MessageCreate(
            role=message.role,
            content=_MESSAGE_CONTENT_ADAPTER.validate_python(
                message.content
            ),
        )

    def _content_to_langchain(
        self,
        contents: list[MessageContent],
    ) -> str:
        parts: list[str] = []

        for item in contents:
            if isinstance(item, TextContent):
                parts.append(item.text)

            elif isinstance(item, PetCardContent):
                parts.append(
                    f"[Pet Card]\n"
                    f"Name: {item.name}\n"
                    f"Pet ID: {item.pet_id}"
                )

        return "\n\n".join(parts)

    async def load(
        self,
        conversation_id: UUID,
    ):
        cache = await self.history_cache_repository.get_history(
            conversation_id=conversation_id
        )

        if cache is None:
            db_messages = await self.message_repository.get_by_conversation(
                conversation_id=conversation_id
            )

            history = [
                self._to_message_create(message)
                for message in db_messages
            ]

            await self.history_cache_repository.set_history(
                conversation_id=conversation_id,
                messages=history,
            )
        else:
            history = cache.messages

        history_messages = []

        for message in history:
            content = self._content_to_langchain(message.content)

            if message.role == "user":
                history_messages.append(
                    HumanMessage(content=content)
                )
            else:
                history_messages.append(
                    AIMessage(content=content)
                )

        return history_messages

    async def save(
        self,
        conversation_id: UUID,
        messages: list[MessageCreate],
    ) -> None:

        # Save DB
        for message in messages:
            await self.message_repository.create(
                conversation_id=conversation_id,
                role=message.role,
                content=[
                    item.model_dump(mode="json")
                    for item in message.content
                ],
            )

        # Update cache
        cache = await self.history_cache_repository.get_history(
            conversation_id=conversation_id
        )

        if cache is None:
            return

        cache.messages.extend(messages)

        await self.history_cache_repository.set_history(
            conversation_id=conversation_id,
            messages=cache.messages,
        )