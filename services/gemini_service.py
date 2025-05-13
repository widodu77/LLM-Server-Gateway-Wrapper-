from services.base import BaseLLMService
from core.models import ChatCompletionRequest, ChatCompletionResponse, TextEmbeddingRequest, TextEmbeddingResponse, ModelInfo, Provider, Message, Role
import os
import httpx
import json
from typing import List, Optional, Dict, Any
import google.generativeai as genai
from datetime import datetime

class GeminiService(BaseLLMService):
    provider = Provider.GEMINI
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        # Initialize the Gemini client
        genai.configure(api_key=self.api_key)
        # Initialize models
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    async def get_chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        # Convert messages to Gemini format
        messages = []
        for msg in request.messages:
            if msg.role == Role.SYSTEM:
                # Gemini doesn't have system messages, so we'll prepend it to the first user message
                if messages and messages[-1]["role"] == Role.USER:
                    messages[-1]["parts"][0]["text"] = f"{msg.content}\n\n{messages[-1]['parts'][0]['text']}"
                continue
            messages.append({
                "role": msg.role,
                "parts": [{"text": msg.content}]
            })

        # Create chat session
        chat = self.model.start_chat(history=messages[:-1] if len(messages) > 1 else [])
        
        # Get response
        response = chat.send_message(
            messages[-1]["parts"][0]["text"] if messages else "",
            generation_config={
                "temperature": request.temperature,
                "top_p": request.top_p,
                "max_output_tokens": request.max_tokens,
                "candidate_count": 1,
            }
        )

        # Convert response to our format
        return ChatCompletionResponse(
            id=f"gemini-{datetime.now().timestamp()}",
            created=int(datetime.now().timestamp()),
            model=request.model,
            choices=[{
                "index": 0,
                "message": {
                    "role": Role.ASSISTANT,
                    "content": response.text
                },
                "finish_reason": "stop"
            }],
            usage={
                "prompt_tokens": int(self.count_tokens(request.messages[-1].content)),
                "completion_tokens": int(self.count_tokens(response.text)),
                "total_tokens": int(self.count_tokens(request.messages[-1].content) + self.count_tokens(response.text))
            },
            provider=self.provider
        )

    async def get_embeddings(self, request: TextEmbeddingRequest) -> TextEmbeddingResponse:
        raise NotImplementedError("Embeddings are not supported by gemini-2.0-flash-lite model")

    async def list_models(self) -> List[ModelInfo]:
        return [
            ModelInfo(
                id="gemini-2.0-flash-lite",
                name="Gemini Flash Lite",
                provider=self.provider,
                capabilities=["chat_completion"],
                max_tokens=32768,
                description="Gemini Flash Lite is a lightweight language model optimized for fast text generation and chat."
            )
        ]

    async def get_model_info(self, model_id: str) -> Optional[ModelInfo]:
        models = await self.list_models()
        for model in models:
            if model.id == model_id:
                return model
        return None

    async def health_check(self) -> bool:
        try:
            # Try to list models as a health check
            await self.list_models()
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
            return TextEmbeddingResponse(
                id=response.get("id", "embedding-response"),
                model=response["model"],
                data=response["data"],
                usage=response["usage"],
                provider=self.provider
            )
        raise ValueError(f"Unsupported request type: {request_type}")

    def count_tokens(self, text: str, model: Optional[str] = None) -> int:
        # This is a rough estimate. For accurate token counting, you should use
        # a proper tokenizer
        return int(len(text.split()) * 1.3)  # Rough estimate: 1.3 tokens per word, rounded to integer 