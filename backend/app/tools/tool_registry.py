from app.tools.compare_pets_tool import ComparePetsTool
from app.tools.find_pets_tool import FindPetsTool
from app.tools.get_pet_tool import GetPetTool


class ToolRegistry:

    def __init__(
        self,
        find_pet: FindPetsTool,
        get_pet: GetPetTool,
        compare_pet: ComparePetsTool,
    ):
        self._tools = {
            "find_pets": find_pet,
            "get_pet": get_pet,
            "compare_pets": compare_pet,
        }

    def get(self, name: str):
        return self._tools[name]

    def langchain(self):
        return [
            tool.as_langchain()
            for tool in self._tools.values()
        ]