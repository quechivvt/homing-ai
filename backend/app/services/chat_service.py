from app.schemas.chat import ChatRequest, ChatResponse
from app.pipelines.pipeline import ChatPipeline

class ChatService:
    def __init__(self, pipeline: ChatPipeline):
        self.pipeline = pipeline

    async def chat(self, request: ChatRequest) -> ChatResponse:
        return await self.pipeline.run(request)






    
                 
        
