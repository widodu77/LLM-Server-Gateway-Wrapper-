from typing import Any, Dict, Optional

class LLMGatewayError(Exception):
    """Base exception for all gateway errors."""
    code: str = "gateway_error"
    status_code: int = 500
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary for API responses."""
        return {
            "error": True,
            "code": self.code,
            "message": self.message,
            "details": self.details
        }

class InvalidRequestError(LLMGatewayError):
    """Exception raised for invalid request parameters."""
    code = "invalid_request"
    status_code = 400

class AuthenticationError(LLMGatewayError):
    """Exception raised for authentication failures."""
    code = "authentication_error"
    status_code = 401

class PermissionError(LLMGatewayError):
    """Exception raised for permission issues."""
    code = "permission_error"
    status_code = 403

class RateLimitError(LLMGatewayError):
    """Exception raised when rate limits are exceeded."""
    code = "rate_limit_exceeded"
    status_code = 429

class ServiceUnavailableError(LLMGatewayError):
    """Exception raised when a service is unavailable."""
    code = "service_unavailable"
    status_code = 503

class ModelNotFoundError(LLMGatewayError):
    """Exception raised when a requested model is not found."""
    code = "model_not_found"
    status_code = 404

class ContentFilterError(LLMGatewayError):
    """Exception raised when content is filtered by a provider."""
    code = "content_filter"
    status_code = 400

class InvalidModelError(LLMGatewayError):
    """Exception raised when an invalid model is requested."""
    code = "invalid_model"
    status_code = 400

class ContextLengthExceededError(LLMGatewayError):
    """Exception raised when the context length is exceeded."""
    code = "context_length_exceeded"
    status_code = 400

class ProviderError(LLMGatewayError):
    """Exception raised when a provider API returns an error."""
    code = "provider_error"
    status_code = 502
    
    def __init__(self, message: str, provider: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.provider = provider
        if details is None:
            self.details = {}
        self.details["provider"] = provider