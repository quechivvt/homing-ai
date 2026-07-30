from app.models.knowledge_chunk import KnowledgeChunk


SOURCE_NAMES = {
    "hanoi_pet_adoption": "Hanoi Pet Adoption",
}


class ContextBuilder:

    @staticmethod
    def build(
        chunks: list[KnowledgeChunk],
    ) -> str:

        contexts = []

        for chunk in chunks:

            metadata = chunk.rawdata or {}

            source = SOURCE_NAMES.get(
                metadata.get("source"),
                metadata.get("source"),
            )

            contexts.append(
                f"""
========== PET ==========

Pet ID:
{metadata.get("pet_id")}

Name:
{metadata.get("name")}

Species:
{metadata.get("species")}

Breed:
{metadata.get("breed")}

Gender:
{metadata.get("gender")}

Source:
{source}

Source Pet ID:
{metadata.get("source_pet_id")}

Detail URL:
{metadata.get("detail_url")}

Image URL:
{metadata.get("image_url")}

Description:
{chunk.content}
""".strip()
            )

        return "\n\n".join(contexts)