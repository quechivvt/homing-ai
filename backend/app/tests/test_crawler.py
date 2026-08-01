import asyncio

from app.crawler.hanoi_pet_adoption import HanoiPetAdoptionCrawler


async def main():
    crawler = HanoiPetAdoptionCrawler()

    pets = await crawler.crawl()


asyncio.run(main())