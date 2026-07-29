from app.models import Message
from app.enum.message_type import MessageType
from app.schemas.chat import (
    ChatMessage,
    TextMessage,
    PetCardMessage,
)
from app.enum.message_role import MessageRole


class MessageMapper:

    @staticmethod
    def to_chat_message(message: Message) -> ChatMessage:
        if message.message_type == MessageType.TEXT:
            return TextMessage(
                role=message.role,
                content=message.content,
            )

        if message.message_type == MessageType.PET_CARD:
            data = message.raw_data or {}

            return PetCardMessage(
                pet_id=data["pet_id"],
                name=data["name"],
                image_url=data["image_url"],
                gender=data["gender"],
                age=data["age"],
                breed=data.get("breed"),
            )

        raise ValueError(f"Unsupported message type: {message.type}")

    @staticmethod
    def to_chat_messages(
        messages: list[Message],
    ) -> list[ChatMessage]:
        return [
            MessageMapper.to_chat_message(message)
            for message in messages
        ]

    @staticmethod
    def from_text(
        *,
        conversation_id,
        role: MessageRole,
        content: str,
    ) -> Message:
        return Message(
            conversation_id=conversation_id,
            role=role,
            type=MessageType.TEXT,
            content=content,
            raw_data=None,
        )

    @staticmethod
    def from_pet_card(
        *,
        conversation_id,
        role: MessageRole,
        pet_card: PetCardMessage,
    ) -> Message:
        return Message(
            conversation_id=conversation_id,
            role=role,
            type=MessageType.PET_CARD,
            content=pet_card.name,
            raw_data={
                "pet_id": str(pet_card.pet_id),
                "name": pet_card.name,
                "image_url": pet_card.image_url,
                "gender": pet_card.gender,
                "age": pet_card.age,
                "breed": pet_card.breed,
            },
        )