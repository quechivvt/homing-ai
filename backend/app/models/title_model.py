from abc import ABC, abstractmethod

class TitleModel(ABC):

    @abstractmethod
    async def generate(
        self,
        user_message: str,
    ) -> str:
        pass