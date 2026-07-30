from pydantic import TypeAdapter

from app.models import Message
from app.schemas.chat import ChatMessage
from app.schemas.message import MessageContent

_CONTENT_ADAPTER = TypeAdapter(list[MessageContent])


class MessageMapper:

    @staticmethod
    def to_chat_message(message: Message) -> ChatMessage:
        return ChatMessage(
            role=message.role,
            content=_CONTENT_ADAPTER.validate_python(
                message.content
            ),
        )

    @staticmethod
    def to_chat_messages(
        messages: list[Message],
    ) -> list[ChatMessage]:
        return [
            MessageMapper.to_chat_message(message)
            for message in messages
        ]