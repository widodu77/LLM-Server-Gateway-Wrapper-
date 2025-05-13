from pydantic_settings import BaseSettings
from typing import Dict, List, Optional, Union
import os
from dotenv import load_dotenv
from core.models import Provider

# Load environment variables from .env file if it exists
load_dotenv()

class Settings(BaseSettings):
    # API settings
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    PROJECT_NAME: str = "LLM Gateway API"
    
    # Provider API keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    COHERE_API_KEY: Optional[str] = os.getenv("COHERE_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Provider endpoints
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    ANTHROPIC_API_BASE: str = "https://api.anthropic.com"
    COHERE_API_BASE: str = "https://api.cohere.ai/v1"
    GOOGLE_API_BASE: str = "https://generativelanguage.googleapis.com/v1beta"
    
    # Default provider
    DEFAULT_PROVIDER: Provider = Provider.OPENAI
    
    # Model mappings between providers
    MODEL_MAPPINGS: Dict[str, Dict[str, str]] = {
        "openai": {
            "default": "gpt-3.5-turbo",
            "gpt-4": "gpt-4",
            "gpt-3.5-turbo": "gpt-3.5-turbo",
        },
        "anthropic": {
            "default": "claude-3-sonnet-20240229",
            "claude-3-opus": "claude-3-opus-20240229",
            "claude-3-sonnet": "claude-3-sonnet-20240229",
            "claude-3-haiku": "claude-3-haiku-20240307",
        },
        "cohere": {
            "default": "command-r-plus",
            "command-r-plus": "command-r-plus",
            "command-r": "command-r",
        },
        "google": {
            "default": "gemini-pro",
            "gemini-pro": "gemini-pro",
            "gemini-2.0-flash-lite": "gemini-2.0-flash-lite",
        },
    }
    
    # Cache settings
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "False").lower() in ("true", "1", "t")
    CACHE_EXPIRY: int = int(os.getenv("CACHE_EXPIRY", "3600"))  # Default 1 hour
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "False").lower() in ("true", "1", "t")
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_TIMEFRAME: int = int(os.getenv("RATE_LIMIT_TIMEFRAME", "3600"))  # Default 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()