# API Versions
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Endpoint paths
CHAT_COMPLETIONS_ENDPOINT = f"{API_PREFIX}/chat/completions"
EMBEDDINGS_ENDPOINT = f"{API_PREFIX}/embeddings"
MODELS_ENDPOINT = f"{API_PREFIX}/models"
HEALTH_ENDPOINT = "/health"

# Error codes
ERROR_INVALID_REQUEST = "invalid_request"
ERROR_AUTHENTICATION = "authentication_error"
ERROR_PERMISSION = "permission_error"
ERROR_RATE_LIMIT = "rate_limit_exceeded"
ERROR_SERVICE_UNAVAILABLE = "service_unavailable"
ERROR_MODEL_NOT_FOUND = "model_not_found"
ERROR_CONTENT_FILTER = "content_filter"
ERROR_INVALID_MODEL = "invalid_model"
ERROR_CONTEXT_LENGTH = "context_length_exceeded"
ERROR_PROVIDER_ERROR = "provider_error"

# Model capabilities
CAPABILITY_CHAT = "chat"
CAPABILITY_EMBEDDINGS = "embeddings"
CAPABILITY_FUNCTION_CALLING = "function_calling"
CAPABILITY_STREAMING = "streaming"

# Provider-specific model mappings for equivalent models
MODEL_MAPPINGS = {
    "gpt-3.5-turbo": {
        "openai": "gpt-3.5-turbo",
        "groq": "llama3-70b-8192",
        "ollama": "llama3"
    },
    "gpt-4": {
        "openai": "gpt-4",
        "groq": "llama3-70b-8192",
        "anthropic": "claude-3-opus-20240229",
        "ollama": "llama3"
    },
    "claude-3-haiku": {
        "anthropic": "claude-3-haiku-20240307",
        "openai": "gpt-3.5-turbo",
        "groq": "llama3-8b-8192",
        "ollama": "llama3"
    },
    "embedding-small": {
        "openai": "text-embedding-3-small",
        "ollama": "nomic-embed-text"
    }
}