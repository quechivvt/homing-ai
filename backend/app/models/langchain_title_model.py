from app.models.title_model import TitleModel
from app.models.chat_model_provider import ChatModelProvider


PROMPT = """
Generate a short conversation title based on the user's messages.

Rules:

- Maximum 6 words.
- Use the user's language.
- Ignore greetings, thanks, and casual small talk.
- Focus on the main topic of the conversation.
- No quotation marks.
- No punctuation.
- Return only the title.

Conversation:

{conversation}
"""


class LangChainTitleModel(TitleModel):

    def __init__(self, provider: ChatModelProvider):
        self.provider = provider

    async def generate(
        self,
        conversation: str,
    ) -> str:

        model = self.provider.chat()

        response = await model.ainvoke(
            PROMPT.format(
                conversation=conversation,
            )
        )

        return response.text().strip()