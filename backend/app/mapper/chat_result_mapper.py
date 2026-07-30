from app.repositories.pet_repository import PetRepository
from app.schemas.chat import ChatResult
from app.schemas.message import (
    MessageCreate,
    MessageRole,
    PetCardContent,
    TextContent,
)


class ChatResultMapper:
    def __init__(
        self,
        pet_repository: PetRepository,
    ):
        self.pet_repository = pet_repository

    async def map(
        self,
        result: ChatResult,
    ) -> MessageCreate:

        content = [
            TextContent(
                text=result.answer,
            )
        ]

        if result.recommended_pet_ids:
            pets = await self.pet_repository.get_by_ids(
                result.recommended_pet_ids
            )

            for pet in pets:
                content.append(
                    PetCardContent(
                        pet_id=pet.id,
                        name=pet.name,
                        image_url=pet.image_url,
                    )
                )

        return MessageCreate(
            role=MessageRole.ASSISTANT,
            content=content,
        )