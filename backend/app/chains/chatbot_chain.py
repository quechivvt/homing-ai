from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
#from app.schemas.chat import ChatResult

model = ChatGoogleGenerativeAI(
    model=settings.GEMINI_MODEL,
    google_api_key=settings.GEMINI_API_KEY,
)

"""model = ChatOpenAI(
    model=settings.GEMINI_MODEL,
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.BASE_URL,
)"""

#structured_model = model.with_structured_output(ChatResult)