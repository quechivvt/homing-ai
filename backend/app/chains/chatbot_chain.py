from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.prompts.chat_prompt import chat_prompt
from app.schemas.chat import ChatResult

model = ChatOpenAI(
    model=settings.GEMINI_MODEL,
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.BASE_URL,
)

structured_model = model.with_structured_output(ChatResult)