import time
import json
import hashlib
from typing import Any, Dict, List, Optional, Union
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/gateway.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("llm_gateway")

def generate_request_id(prefix: str = "req") -> str:
    """Generate a unique request ID."""
    timestamp = int(time.time() * 1000)
    random_salt = hashlib.md5(str(timestamp).encode()).hexdigest()[:6]
    return f"{prefix}_{timestamp}_{random_salt}"

def calculate_cache_key(provider: str, request_data: Dict[str, Any]) -> str:
    """Calculate a cache key for a request."""
    # Remove non-deterministic fields like timestamps or request IDs
    cache_data = request_data.copy()
    if "stream" in cache_data:
        cache_data.pop("stream")  # Don't cache streaming requests with the same key
    
    # Sort the dictionary to ensure consistent serialization
    serialized = json.dumps(cache_data, sort_keys=True)
    
    # Create a hash of the serialized data
    hash_key = hashlib.md5(serialized.encode()).hexdigest()
    
    return f"{provider}:{hash_key}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length for logging."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_log_messages(messages: List[Dict[str, Any]]) -> str:
    """Format chat messages for logging."""
    formatted = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = truncate_text(str(msg.get("content", "")))
        formatted.append(f"{role}: {content}")
    
    return " | ".join(formatted)

def get_model_mapping(requested_model: str, provider: str, fallback_model: Optional[str] = None) -> str:
    """
    Get the equivalent model for a provider based on the requested model.
    If no mapping exists, returns the fallback model or the requested model.
    """
    from core.constants import MODEL_MAPPINGS
    
    # Check if we have a mapping for this model
    if requested_model in MODEL_MAPPINGS:
        provider_mappings = MODEL_MAPPINGS[requested_model]
        if provider in provider_mappings:
            return provider_mappings[provider]
    
    # If no mapping exists, return the fallback or the original
    return fallback_model or requested_model