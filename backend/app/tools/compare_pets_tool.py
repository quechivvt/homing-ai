from app.schemas.pet import PetResponse
from app.repositories.pet_repository import PetRepository
from langchain_core.tools import StructuredTool

class ComparePetsTool:
    name ="compare_pets"
    description = "Compare multiple pets by their ids."

    def __init__(
        self,
        repository: PetRepository,
    ):
        self.repository = repository

    async def invoke(
        self,
        pet_ids: list[int],
    ) -> list[PetResponse]:

        pets = await self.repository.get_by_ids(
            pet_ids
        )

        return [PetResponse.model_validate(p)
        for p in pets]
    
    def as_langchain(self):
        return StructuredTool.from_function(
            coroutine=self.invoke,
            name=self.name,
            description=self.description,
        )