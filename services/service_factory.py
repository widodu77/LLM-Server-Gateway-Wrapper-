'''
from services.openai_service import OpenAIService
# from services.anthropic_service import AnthropicService
# from services.groq_service import GroqService
# from services.ollama_service import OllamaService
from core.models import Provider

class LLMServiceFactory:
    def __init__(self):
        self._services = {
            Provider.OPENAI: OpenAIService(),
            # Provider.ANTHROPIC: AnthropicService(),
            # Provider.GROQ: GroqService(),
            # Provider.OLLAMA: OllamaService(),
        }
    
    def get_service(self, provider: Provider):
        return self._services.get(provider)
    
    def get_default_service(self):
        default_provider = list(self._services.keys())[0]
        return self.get_service(default_provider)
    
    def get_available_providers(self):
        return list(self._services.keys())

service_factory = LLMServiceFactory()
'''
from typing import Dict, Type
from config import settings

# Import service classes
from services.openai_service import OpenAIService
from services.gemini_service import GeminiService

# Service registry maps provider names to their service classes
SERVICE_REGISTRY: Dict[str, Type] = {
    "openai": OpenAIService,
    "gemini": GeminiService,
}

def get_service(provider_name: str):
    """
    Factory function to get the appropriate service instance for a provider.
    
    Args:
        provider_name: Name of the provider (e.g., "openai", "gemini")
        
    Returns:
        An instance of the appropriate service class
    
    Raises:
        ValueError: If the provider is not supported
    """
    if provider_name not in SERVICE_REGISTRY:
        raise ValueError(f"Unsupported provider: {provider_name}")
    
    service_class = SERVICE_REGISTRY[provider_name]
    return service_class()
