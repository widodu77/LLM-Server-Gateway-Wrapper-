from fastapi import APIRouter, Body, HTTPException, BackgroundTasks, Depends
from core.models import ChatCompletionRequest, ChatCompletionResponse
from services import service_factory
from config import settings
# Assume get_cache is a dependency that returns a cache instance if enabled.
from api.dependencies import get_cache

router = APIRouter()

@router.post("/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(
    background_tasks: BackgroundTasks,
    request: ChatCompletionRequest = Body(...),
    cache = Depends(get_cache)
):
    # Use provider in request or default provider from configuration.
    provider_name = request.provider or settings.DEFAULT_PROVIDER.lower()

    # Retrieve the appropriate service adapter from the factory.
    service = service_factory.get_service(provider_name)
    if not service:
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{provider_name}' not available."
        )

    # Optional: check and get cached responses if caching is enabled.
    if settings.ENABLE_CACHE and cache and not request.stream:
        cache_key = f"chat:{provider_name}:{hash(str(request.dict()))}"
        cached_response = await cache.get(cache_key)
        if cached_response:
            return cached_response

    # Call the service method to get the chat completion.
    response = await service.get_chat_completion(request)

    # Cache the result if applicable.
    if settings.ENABLE_CACHE and cache and not request.stream:
        background_tasks.add_task(
            cache.set, cache_key, response, expiry=settings.CACHE_EXPIRATION
        )

    return response
