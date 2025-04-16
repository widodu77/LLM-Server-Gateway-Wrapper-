from services.base import BaseLLMService
from core.models import ChatCompletionRequest, ChatCompletionResponse, TextEmbeddingRequest, TextEmbeddingResponse, ModelInfo, Provider
import os

class OpenAIService(BaseLLMService):
    provider = Provider.OPENAI

    async def get_chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        # Convert the standardized request to OpenAI's required format
        payload = self.convert_request(request)
        
        # Read your API key from your settings or environment variables
        api_key=os.getenv("OPENAI_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def get_embeddings(self, request: TextEmbeddingRequest) -> TextEmbeddingResponse:
        # Implement OpenAI embeddings call
        return TextEmbeddingResponse(
            model=request.model,
            data=[{"embedding": [0.1, 0.2, 0.3]}],
            provider="openai"
        )

    async def list_models(self) -> list[ModelInfo]:
        # Return a list of available models for OpenAI
        return []

    async def get_model_info(self, model_id: str) -> ModelInfo:
        # Return specific model information
        return ModelInfo(model_id=model_id, provider="openai", description="Mock model")

    async def health_check(self) -> bool:
        # Check connectivity, return True if healthy
        return True

    def convert_request(self, request):
        # Convert the standardized request to OpenAI's format
        return request.dict()

    def convert_response(self, response: dict, request_type: str):
        # Convert OpenAI's response into the standardized response format
        if request_type == "chat":
            return ChatCompletionResponse(**response)
        else:
            return TextEmbeddingResponse(**response)

    def count_tokens(self, text: str, model: str = None) -> int:
        # Rough estimate of token count, adjust as needed
        return len(text.split())
