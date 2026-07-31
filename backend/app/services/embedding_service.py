from langchain_google_genai import GoogleGenerativeAIEmbeddings
import asyncio

from app.core.config import settings

#embeddings = GoogleGenerativeAIEmbeddings(
#            model=settings.EMBEDDING_MODEL,
#            google_api_key=settings.GEMINI_API_KEY,
#        )

class EmbeddingService:

    BATCH_SIZE = 50
    BATCH_DELAY = 1.0

    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY,)

    async def embed_query(
        self,
        text: str,
    ) -> list[float]:
        return await self.embeddings.aembed_query(text)

    async def embed_document(
        self,
        text: str,
    ) -> list[float]:
        return (await self.embed_documents([text]))[0]

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        vectors: list[list[float]] = []

        for start in range(0, len(texts), self.BATCH_SIZE):

            batch = texts[start:start + self.BATCH_SIZE]

            result = await self.embeddings.aembed_documents(batch)

            vectors.extend(result)

            if start + self.BATCH_SIZE < len(texts):
                await asyncio.sleep(self.BATCH_DELAY)

        return vectors