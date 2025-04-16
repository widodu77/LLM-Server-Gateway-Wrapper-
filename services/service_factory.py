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
