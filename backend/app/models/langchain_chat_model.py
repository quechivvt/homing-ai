from app.models.chat_model import ChatModel
from app.schemas.stream_event import TokenEvent
from app.models.chat_model_provider import ChatModelProvider
from app.tools.tool_executor import ToolExecutor
from langchain_core.messages import AIMessage, ToolMessage
from app.schemas.stream_event import ToolStartEvent, ToolEndEvent, PetCardEvent, DoneEvent

class LangChainChatModel(ChatModel):

    def __init__(self, 
        provider :ChatModelProvider,
        executor: ToolExecutor,
        ):
        self.provider = provider
        self.executor = executor

    def _extract_text(self, content) -> str:
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            return "".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
                and block.get("type") == "text"
            )

        return str(content)

    async def invoke(self, messages):

        model = self.provider.chat()

        while True:

            response = await model.ainvoke(messages)

            if not response.tool_calls:
                return response

            messages.append(response)

            for tool_call in response.tool_calls:

                result = await self.executor.execute(tool_call)

                tool_message = ToolMessage(
                    tool_call_id=tool_call["id"],
                    content=self.executor.serialize(result),
                )

                messages.append(tool_message)


    async def stream(self, messages):
        model = self.provider.chat()
        while True:
            tool_calls = []
            async for chunk in model.astream(messages):
                if chunk.tool_calls:
                    tool_calls.extend(chunk.tool_calls)
                if chunk.content:
                    text = self._extract_text(chunk.content)
                    if text:
                        yield TokenEvent(
                            token=text
                        )
            if not tool_calls:
                yield DoneEvent()
                return
            messages.append(
                AIMessage(
                    content=[],
                    tool_calls=tool_calls,
                )
            )

            for tool_call in tool_calls:
                print(">>> ToolStartEvent")
                yield ToolStartEvent(
                    tool=tool_call["name"]
                )
                
                try:
                    result = await self.executor.execute(tool_call)
                    print(result)

                    if isinstance(result, list):
                        for pet in result:
                            yield PetCardEvent(pet=pet)
                    elif result is not None:
                        yield PetCardEvent(pet=result)

                    messages.append(
                        ToolMessage(
                            tool_call_id=tool_call["id"],
                            content=self.executor.serialize(result),
                        )
                    )

                finally:
                    print(">>> ToolEndEvent")
                    yield ToolEndEvent(
                        tool=tool_call["name"]
                    )