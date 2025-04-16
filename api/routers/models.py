from fastapi import APIRouter, HTTPException
from core.models import ModelInfo
from services import service_factory
from config import settings

router = APIRouter()

@router.get("", response_model=list[ModelInfo])
async def list_models(provider: str = None):
    provider_name = provider or settings.DEFAULT_PROVIDER.lower()
    service = service_factory.get_service(provider_name)
    if not service:
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{provider_name}' not available."
        )
    models = await service.list_models()
    return models

@router.get("/{model_id}", response_model=ModelInfo)
async def get_model_info(model_id: str, provider: str = None):
    provider_name = provider or settings.DEFAULT_PROVIDER.lower()
    service = service_factory.get_service(provider_name)
    if not service:
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{provider_name}' not available."
        )
    model_info = await service.get_model_info(model_id)
    if not model_info:
        raise HTTPException(status_code=404, detail="Model not found")
    return model_info
