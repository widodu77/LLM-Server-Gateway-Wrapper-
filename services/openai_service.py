from services.base import BaseLLMService
from core.models import ChatCompletionRequest, ChatCompletionResponse, TextEmbeddingRequest, TextEmbeddingResponse, ModelInfo, Provider
import os
import httpx
import json
from typing import List, Optional, Dict, Any

class OpenAIService(BaseLLMService):
    provider = Provider.OPENAI
    BASE_URL = "https://api.openai.com/v1"
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        payload = self.convert_request(request)
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/chat/completions",
                json=payload,
                headers=self.headers,
            )
            resp.raise_for_status()
            data = resp.json()

        return self.convert_response(data, request_type="chat")

    async def get_embeddings(self, request: TextEmbeddingRequest) -> TextEmbeddingResponse:
        payload = {
            "model": request.model,
            "input": request.input
        }
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.BASE_URL}/embeddings",
                json=payload,
                headers=self.headers,
            )
            resp.raise_for_status()
            data = resp.json()

        return self.convert_response(data, request_type="embedding")

    async def list_models(self) -> List[ModelInfo]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.BASE_URL}/models",
                headers=self.headers,
            )
            resp.raise_for_status()
            data = resp.json()
            
        models = []
        for model in data["data"]:
            models.append(ModelInfo(
                id=model["id"],
                name=model["id"],
                provider=self.provider,
                capabilities=["chat_completion", "embeddings"] if "gpt" in model["id"].lower() else ["embeddings"],
                max_tokens=model.get("context_length", None),
                description=model.get("description", "")
            ))
        return models

    async def get_model_info(self, model_id: str) -> Optional[ModelInfo]:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    f"{self.BASE_URL}/models/{model_id}",
                    headers=self.headers,
                )
                resp.raise_for_status()
                data = resp.json()
                
                return ModelInfo(
                    id=data["id"],
                    name=data["id"],
                    provider=self.provider,
                    capabilities=["chat_completion", "embeddings"] if "gpt" in data["id"].lower() else ["embeddings"],
                    max_tokens=data.get("context_length", None),
                    description=data.get("description", "")
                )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.BASE_URL}/models",
                    headers=self.headers,
                )
                resp.raise_for_status()
                return True
        except Exception:
            return False

    def convert_request(self, request: Any) -> Dict[str, Any]:
        if isinstance(request, ChatCompletionRequest):
            return {
                "model": request.model,
                "messages": [msg.model_dump() for msg in request.messages],
                "temperature": request.temperature,
                "top_p": request.top_p,
                "max_tokens": request.max_tokens,
                "stream": request.stream,
                "frequency_penalty": request.frequency_penalty,
                "presence_penalty": request.presence_penalty,
                "stop": request.stop,
                "user": request.user,
                "functions": request.functions,
                "function_call": request.function_call
            }
        elif isinstance(request, TextEmbeddingRequest):
            return {
                "model": request.model,
                "input": request.input
            }
        raise ValueError(f"Unsupported request type: {type(request)}")

    def convert_response(self, response: Dict[str, Any], request_type: str) -> Any:
        if request_type == "chat":
            return ChatCompletionResponse(
                id=response["id"],
                created=response["created"],
                model=response["model"],
                choices=response["choices"],
                usage=response.get("usage"),
                provider=self.provider
            )
        elif request_type == "embedding":
            usage = response["usage"]
            if "completion_tokens" not in usage:
                usage = usage.copy()
                usage["completion_tokens"] = 0
            return TextEmbeddingResponse(
                id=response.get("id", "embedding-response"),
                model=response["model"],
                data=response["data"],
                usage=usage,
                provider=self.provider
            )
        raise ValueError(f"Unsupported request type: {request_type}")

    def count_tokens(self, text: str, model: Optional[str] = None) -> int:
        # This is a rough estimate. For accurate token counting, you should use tiktoken
        # or the OpenAI tokenizer
        return len(text.split()) * 1.3  # Rough estimate: 1.3 tokens per word
