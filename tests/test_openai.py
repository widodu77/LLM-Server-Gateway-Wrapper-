import os
print("OPENAI_API_KEY from env:", os.getenv("OPENAI_API_KEY"))


import pytest
import os
from services.openai_service import OpenAIService
from core.models import ChatCompletionRequest, Message, Role, TextEmbeddingRequest

@pytest.fixture
def openai_service():
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
    return OpenAIService()

@pytest.mark.asyncio
async def test_chat_completion(openai_service):
    request = ChatCompletionRequest(
        model="gpt-3.5-turbo",
        messages=[
            Message(role=Role.USER, content="Say hello!")
        ]
    )
    response = await openai_service.get_chat_completion(request)
    assert response.model.startswith("gpt-3.5-turbo")
    assert len(response.choices) > 0
    assert response.choices[0].message.content
    assert response.provider == "openai"

@pytest.mark.asyncio
async def test_embeddings(openai_service):
    request = TextEmbeddingRequest(
        model="text-embedding-ada-002",
        input="Hello, world!"
    )
    response = await openai_service.get_embeddings(request)
    assert response.model.startswith("text-embedding-ada-002")
    assert len(response.data) > 0
    assert len(response.data[0].embedding) > 0
    assert response.provider == "openai"

@pytest.mark.asyncio
async def test_list_models(openai_service):
    models = await openai_service.list_models()
    assert len(models) > 0
    assert any(model.id == "gpt-3.5-turbo" for model in models)

@pytest.mark.asyncio
async def test_get_model_info(openai_service):
    model = await openai_service.get_model_info("gpt-3.5-turbo")
    assert model is not None
    assert model.id == "gpt-3.5-turbo"
    assert "chat_completion" in model.capabilities

@pytest.mark.asyncio
async def test_health_check(openai_service):
    assert await openai_service.health_check() is True 