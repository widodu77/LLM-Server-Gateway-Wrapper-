from typing import Dict, List, Optional, Union, Any
from enum import Enum
from pydantic import BaseModel, Field

class Provider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    OLLAMA = "ollama"

class Role(str, Enum):
    """Message role types."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

class Message(BaseModel):
    """A message in a chat conversation."""
    role: Role
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None

class ModelInfo(BaseModel):
    """Information about an LLM model."""
    id: str
    name: str
    provider: Provider
    capabilities: List[str] = Field(default_factory=list)
    max_tokens: Optional[int] = None
    description: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    """Standardized chat completion request."""
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    provider: Optional[Provider] = None
    frequency_penalty: Optional[float] = 0
    presence_penalty: Optional[float] = 0
    stop: Optional[Union[str, List[str]]] = None
    user: Optional[str] = None
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[Union[str, Dict[str, Any]]] = None

class ChatCompletionResponseChoice(BaseModel):
    """A choice in a chat completion response."""
    index: int
    message: Message
    finish_reason: Optional[str] = None

class Usage(BaseModel):
    """Token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    """Standardized chat completion response."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: Optional[Usage] = None
    provider: Provider

class TextEmbeddingRequest(BaseModel):
    """Standardized text embedding request."""
    model: str
    input: Union[str, List[str]]
    provider: Optional[Provider] = None
    user: Optional[str] = None

class Embedding(BaseModel):
    """A single text embedding."""
    index: int
    embedding: List[float]
    object: str = "embedding"

class TextEmbeddingResponse(BaseModel):
    """Standardized text embedding response."""
    id: str
    object: str = "list"
    data: List[Embedding]
    model: str
    usage: Usage
    provider: Provider

class ErrorResponse(BaseModel):
    """Standardized error response."""
    error: bool = True
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None