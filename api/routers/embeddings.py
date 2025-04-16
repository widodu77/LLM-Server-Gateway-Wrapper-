from fastapi import APIRouter, Body, HTTPException
from core.models import TextEmbeddingRequest, TextEmbeddingResponse
from services import service_factory
from config import settings

router = APIRouter()

@router.post("", response_model=TextEmbeddingResponse)
async def create_text_embedding(request: TextEmbeddingRequest = Body(...)):
    provider_name = request.provider or settings.DEFAULT_PROVIDER.lower()
    service = service_factory.get_service(provider_name)

    if not service:
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{provider_name}' not available."
        )
    
    response = await service.get_embeddings(request)
    return response
