from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.prompts.chat_prompt import chat_prompt
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(
    model=settings.GEMINI_MODEL,
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.BASE_URL,
)

parser = StrOutputParser()

chat_chain = chat_prompt | model | parser

#model = ChatGoogleGenerativeAI(
#    model=settings.GEMINI_MODEL,
#    google_api_key=settings.GEMINI_API_KEY,
#)


