import json

from app.schemas.chat import ChatRequest, ChatResponse
from app.pipelines.pipeline import ChatPipeline
from fastapi.responses import StreamingResponse
from app.builders.stream_encode import StreamEncoder

class ChatService:
    def __init__(self, pipeline: ChatPipeline):
        self.pipeline = pipeline

    async def chat(self, request: ChatRequest) -> ChatResponse:
        return await self.pipeline.run(request)

    async def stream(
        self,
        request: ChatRequest,
    ):

        async def event_generator():
            async for event in self.pipeline.stream(request):
                yield (
                    StreamEncoder.encode(event=event)
                )

        return StreamingResponse(
            event_generator(),
            media_type="application/x-ndjson",
        )






    
                 
        
