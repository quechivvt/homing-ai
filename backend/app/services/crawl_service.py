from app.crawler.hanoi_pet_adoption import HanoiPetAdoptionCrawler
from app.models import Pet


class CrawlService:
    def __init__(self, db, pet_repository):
        self.db = db
        self.pet_repository = pet_repository

    async def crawl_hanoi_pet_adoption(self) -> int:

        crawler = HanoiPetAdoptionCrawler()

        pet_dicts = await crawler.crawl()

        pets = [
            Pet(**pet)
            for pet in pet_dicts
        ]

        await self.pet_repository.upsert_many(pets)

        await self.db.commit()

        return len(pets)