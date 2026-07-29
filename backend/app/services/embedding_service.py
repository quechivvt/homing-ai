from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings

class EmbeddingService:

    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
        )

    async def embed_document(
        self,
        text: str,
    ) -> list[float]:
        vectors = await self.embeddings.aembed_documents([text])
        return vectors[0]

    async def embed_query(
        self,
        text: str,
    ) -> list[float]:
        return await self.embeddings.aembed_query(text)