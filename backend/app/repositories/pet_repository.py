from sqlalchemy import select

from app.models import Pet
from app.repositories.base_repository import BaseRepository


class PetRepository(BaseRepository[Pet]):
    def __init__(self, db):
        super().__init__(db, Pet)

    async def get_by_source(
        self,
        source: str,
        source_id: str,
    ) -> Pet | None:

        result = await self.db.execute(
            select(Pet).where(
                Pet.source == source,
                Pet.source_id == source_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_available(
        self,
    ) -> list[Pet]:

        result = await self.db.execute(
            select(Pet)
            .where(
                Pet.available.is_(True)
            )
        )

        return list(result.scalars().all())

    async def upsert_many(
        self,
        pets: list[Pet],
    ) -> list[Pet]:

        results: list[Pet] = []

        for new_pet in pets:
            pet = await self.get_by_source(
                new_pet.source,
                new_pet.source_id,
            )

            if pet is None:
                await self.add(new_pet)
                results.append(new_pet)
                continue

            for column in self.model.__table__.columns:
                name = column.name

                if name in ("id", "created_at","updated_at"):
                    continue

                setattr(
                    pet,
                    name,
                    getattr(new_pet, name),
                )

            await self.flush(pet)
            results.append(pet)

        return results