from abc import ABC, abstractmethod

class Tool(ABC):

    @abstractmethod
    async def invoke(self, **kwargs):
        ...