import pytest
import os
from services.gemini_service import GeminiService
from core.models import ChatCompletionRequest, Message, Role, TextEmbeddingRequest

@pytest.fixture
def gemini_service():
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY not set")
    return GeminiService()

@pytest.mark.asyncio
async def test_chat_completion(gemini_service):
    request = ChatCompletionRequest(
        model="gemini-2.0-flash-lite",
        messages=[
            Message(role=Role.USER, content="Say hello!")
        ]
    )
    response = await gemini_service.get_chat_completion(request)
    assert response.model == "gemini-2.0-flash-lite"
    assert len(response.choices) > 0
    assert response.choices[0].message.content
    assert response.provider == "gemini"
    assert isinstance(response.usage.prompt_tokens, int)
    assert isinstance(response.usage.completion_tokens, int)
    assert isinstance(response.usage.total_tokens, int)

@pytest.mark.asyncio
async def test_embeddings(gemini_service):
    request = TextEmbeddingRequest(
        model="gemini-2.0-flash-lite",
        input="Hello, world!"
    )
    with pytest.raises(NotImplementedError):
        await gemini_service.get_embeddings(request)

@pytest.mark.asyncio
async def test_list_models(gemini_service):
    models = await gemini_service.list_models()
    assert len(models) > 0
    assert any(model.id == "gemini-2.0-flash-lite" for model in models)
    model = next(m for m in models if m.id == "gemini-2.0-flash-lite")
    assert "chat_completion" in model.capabilities
    assert "embeddings" not in model.capabilities

@pytest.mark.asyncio
async def test_get_model_info(gemini_service):
    model = await gemini_service.get_model_info("gemini-2.0-flash-lite")
    assert model is not None
    assert model.id == "gemini-2.0-flash-lite"
    assert "chat_completion" in model.capabilities
    assert "embeddings" not in model.capabilities

@pytest.mark.asyncio
async def test_health_check(gemini_service):
    assert await gemini_service.health_check() is True 