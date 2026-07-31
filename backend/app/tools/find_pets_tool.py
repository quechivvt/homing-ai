from app.schemas.pet import PetResponse
from app.repositories.pet_repository import PetRepository
from langchain_core.tools import StructuredTool

class FindPetsTool:

    name = "find_pets"

    description = (
        "Find pets matching user preferences such as "
        "species, breed, age, color or gender."
    )

    def __init__(
        self,
        repository: PetRepository,
    ):
        self.repository = repository

    async def invoke(
        self,
        name: str | None = None,
        species: str | None = None,
        breed: str | None = None,
        color: str | None = None,
        gender: str | None = None,
        age: str | None = None,
        available: bool = True,
        limit: int = 10,
    ) -> list[PetResponse]:

        pets = await self.repository.find(
            name=name,
            species=species,
            breed=breed,
            color=color,
            gender=gender,
            age=age,
            available=available,
            limit=limit,
        )

        return [
            PetResponse.model_validate(p)
            for p in pets
        ]

    def as_langchain(self):
        return StructuredTool.from_function(
            coroutine=self.invoke,
            name=self.name,
            description=self.description,
        )