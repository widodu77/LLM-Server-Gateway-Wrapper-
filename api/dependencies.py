from functools import lru_cache
from typing import Optional, Dict, Any
import hashlib
import json
from datetime import datetime, timedelta
from fastapi import Depends, Header, HTTPException, Request
from config import settings

# Simple in-memory cache implementation
class SimpleCache:
    def __init__(self, expiry_seconds: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.expiry_seconds = expiry_seconds
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            entry = self.cache[key]
            if datetime.utcnow() < entry["expiry"]:
                return entry["value"]
            else:
                # Expired entry
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        expiry = datetime.utcnow() + timedelta(seconds=self.expiry_seconds)
        self.cache[key] = {"value": value, "expiry": expiry}
    
    def clear(self) -> None:
        self.cache.clear()

# Create a global cache instance
_cache = SimpleCache(expiry_seconds=settings.CACHE_EXPIRY)

def generate_cache_key(request_data: Dict[str, Any]) -> str:
    """Generate a deterministic cache key from request data."""
    # Sort the dictionary to ensure consistent ordering
    serialized = json.dumps(request_data, sort_keys=True)
    return hashlib.md5(serialized.encode()).hexdigest()

@lru_cache()
def get_cache():
    """Dependency to get cache instance."""
    if settings.ENABLE_CACHE:
        return _cache
    return None

# Additional dependencies that might be needed
async def get_api_key(x_api_key: Optional[str] = Header(None)):
    """Validate API key if required."""
    # Implement API key validation logic if needed
    # For now, return nothing (no validation)
    return x_api_key

async def check_rate_limit(request: Request):
    """Check rate limiting."""
    # Implement rate limiting logic if needed
    # For now, do nothing
    if settings.RATE_LIMIT_ENABLED:
        # You could implement rate limiting based on IP, API key, etc.
        pass
    return True