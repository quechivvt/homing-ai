import asyncio

from app.core.database import AsyncSessionLocal
from app.repositories.pet_repository import PetRepository
from app.services.crawl_service import CrawlService


async def main():
    async with AsyncSessionLocal() as db:
        service = CrawlService(
            db=db,
            pet_repository=PetRepository(db),
        )

        count = await service.crawl_hanoi_pet_adoption()

        print(f"Seeded {count} pets")


if __name__ == "__main__":
    asyncio.run(main())