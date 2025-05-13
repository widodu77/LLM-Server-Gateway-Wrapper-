from fastapi import APIRouter, Body, HTTPException, BackgroundTasks, Depends
from core.models import ChatCompletionRequest, ChatCompletionResponse
from services import service_factory
from config import settings

router = APIRouter()

@router.post("/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest = Body(...)):
    # Use provider in request or default provider from configuration.
    provider_name = request.provider or settings.DEFAULT_PROVIDER.lower()

    # Retrieve the appropriate service adapter from the factory.
    service = service_factory.get_service(provider_name)
    if not service:
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{provider_name}' not available."
        )

    # Call the service method to get the chat completion.
    response = await service.get_chat_completion(request)
   
    return response
