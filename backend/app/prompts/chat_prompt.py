from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.core.config import settings

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", settings.SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)