from app.tools.tool_registry import ToolRegistry
from pydantic import BaseModel
import json

class ToolExecutor:

    def __init__(
        self,
        registry: ToolRegistry,
    ):
        self.registry = registry

    async def execute(self, tool_call):
        tool = self.registry.get(tool_call["name"])

        return await tool.invoke(**tool_call["args"])

    def serialize(self, result) -> str:
        if isinstance(result, BaseModel):
            payload = result.model_dump(mode="json")

        elif isinstance(result, list):
            payload = [
                item.model_dump(mode="json")
                if isinstance(item, BaseModel)
                else item
                for item in result
            ]

        else:
            payload = result

        return json.dumps(
            payload,
            ensure_ascii=False,
        )