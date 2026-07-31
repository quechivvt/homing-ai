from app.models.pet import Pet
from app.schemas.pet import PetResponse
from app.repositories.pet_repository import PetRepository
from langchain_core.tools import StructuredTool

class GetPetTool:
    name ="get_pet"
    description = "Get detailed information about a pet by its id."

    def __init__(
        self,
        repository: PetRepository,
    ):
        self.repository = repository

    async def invoke(
        self,
        pet_id: int,
    ) -> Pet | None:

        pet = await self.repository.get_by_id(
            pet_id
        )
        return PetResponse.model_validate(pet)

    def as_langchain(self):
        return StructuredTool.from_function(
            coroutine=self.invoke,
            name=self.name,
            description=self.description,
        )