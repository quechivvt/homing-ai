from __future__ import annotations

import json
from typing import Any

import httpx
from bs4 import BeautifulSoup


class HanoiPetAdoptionCrawler:
    FILTER_URL = "https://www.hanoipetadoption.com/en/filter-pet"

    PET_TYPES = {
        5: "dog",
        6: "cat",
    }

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            timeout=30,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/138.0 Safari/537.36"
                )
            },
            follow_redirects=True,
        )

    async def crawl(self) -> list[dict[str, Any]]:
        pets = []

        for pet_type_id in (5, 6):
            page = 1

            while True:
                html = await self.fetch_list(
                    pet_type_id,
                    page,
                )

                summaries = self.parse_list(
                    html,
                    pet_type_id,
                )

                if not summaries:
                    break

                for summary in summaries:
                    detail_html = await self.fetch_detail(
                        summary["detail_url"]
                    )

                    pets.append(
                        self.parse_detail(
                            summary,
                            detail_html,
                        )
                    )

                print(
                    f"PetType={pet_type_id}, Page={page}, Count={len(summaries)}"
                )

                page += 1

        return pets

    async def fetch_list(
        self,
        pet_type_id: int,
        page: int,
    ) -> str:

        payload = {
            "PetTypeId": str(pet_type_id),
            "CurrentPage": str(page),
        }

        response = await self.client.post(
            self.FILTER_URL,
            data=payload,
        )

        response.raise_for_status()

        data = response.json()

        html = (
            data["Result"]
            .replace("\\u003c", "<")
            .replace("\\u003e", ">")
            .replace('\\"', '"')
        )

        return html

    async def fetch_detail(
        self,
        url: str,
    ) -> str:

        response = await self.client.get(url)
        response.raise_for_status()

        return response.text

    def parse_list(
        self,
        html: str,
        pet_type_id: int,
    ) -> list[dict[str, Any]]:

        soup = BeautifulSoup(html, "html.parser")

        pets = []

        for card in soup.select(".adopt-card"):

            link = card.select_one(".caption-adoption h5 a")

            if link is None:
                continue

            image = card.select_one(".adopt-image img")

            pets.append(
                {
                    "name": link.get_text(strip=True),
                    "detail_url": link["href"],
                    "image_url": (
                        image.get("src")
                        if image
                        else None
                    ),
                    "species": self.PET_TYPES[
                        pet_type_id
                    ],
                }
            )

        return pets

    def parse_detail(
        self,
        summary: dict[str, Any],
        html: str,
    ) -> dict[str, Any]:

        soup = BeautifulSoup(html, "html.parser")

        info = {}

        for li in soup.select(
            ".caption-adoption > ul > li"
        ):

            strong = li.find("strong")

            if strong is None:
                continue

            key = (
                strong.get_text(strip=True)
                .replace(":", "")
                .strip()
            )

            value = (
                li.get_text(" ", strip=True)
                .replace(
                    strong.get_text(strip=True),
                    "",
                    1,
                )
                .strip()
            )

            info[key] = value

        status = {}

        for row in soup.select(".info-animal .row"):

            icon = row.select_one("i")
            label = row.select_one("span")

            if icon is None or label is None:
                continue

            classes = icon.get("class", [])

            if "fa-check-circle" in classes:
                value = True
            elif "fa-times-circle" in classes:
                value = False
            else:
                value = None

            status[
                label.get_text(strip=True)
            ] = value

        contacts = []

        for person in soup.select(
            ".contact-adoption > div"
        ):

            link = person.select_one("a")

            if link is None:
                continue

            contacts.append(
                {
                    "name": link.get_text(strip=True),
                    "url": link["href"],
                }
            )

        gallery = []

        for img in soup.select(
            ".image-gallery img"
        ):

            url = (
                img.get("data-src")
                or img.get("src")
            )

            if url:
                gallery.append(url)

        description = ""

        section = soup.select_one(
            ".animal-description"
        )

        if section:
            description = section.get_text(
                "\n",
                strip=True,
            )

        slug = (
            summary["detail_url"]
            .rstrip("/")
            .split("/")[-1]
        )

        source_id = slug.split("-")[-1]

        return {
            "source": "hanoi_pet_adoption",
            "source_id": source_id,
            "detail_url": summary["detail_url"],
            "image_url": summary["image_url"],
            "name": summary["name"],
            "species": summary["species"],
            "breed": info.get("Breed"),
            "color": info.get("Color"),
            "gender": info.get("Gender"),
            "age": info.get("Age"),
            "weight": info.get("Weight"),
            "vaccination": status.get("Vaccination"),
            "chip": info.get("Chip"),
            "online_adoption_available": (
                info.get("Receive Online", "")
                .strip()
                .lower()
                == "yes"
            ),
            "contact_adoption": contacts,
            "description": description,
            "available": True,
            "raw_data": {
                "info": info,
                "status": status,
                "gallery": gallery,
            },
        }

    async def close(self):
        await self.client.aclose()