# LLM Gateway API

A unified API gateway for multiple Large Language Model (LLM) providers. This project allows you to interact with different LLM APIs (OpenAI and Google's Gemini) through a single, standardized REST API.

## Features
- Unified API for chat completions, text embeddings, and model info
- Standardized request/response formats
- Easy provider switching (OpenAI, Gemini)
- Built with FastAPI (async, high performance)
- Ready for extension and production use

## How It Works
- The API exposes endpoints for chat completions, embeddings, and model info
- Each provider is implemented as a service class
- The API routes requests to the correct provider based on your request or configuration
- Responses are normalized to a common schema

## Stuff to add
- Add middleware that would take care of token usage
- Add caching 

## Project Structure
```
llmops-gateway/
├── api/              # FastAPI routers and dependencies
├── core/             # Shared data models (Pydantic)
├── services/         # Provider service implementations
├── tests/            # Test suite
├── main.py           # FastAPI app entry point
├── config.py         # Configuration and settings
├── requirements.txt  # Python dependencies
├── README.md         # This file
```

## Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd llmops-gateway
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your environment variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_PROVIDER=gemini  # or openai
ENABLE_CACHE=false
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

### 5. Access the API docs
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser for the interactive Swagger UI.

## Provider-Specific Notes

### OpenAI
- Supports both chat completions and embeddings
- Models: gpt-3.5-turbo, gpt-4

### Gemini
- Currently supports chat completions only
- Models: gemini-2.0-flash-lite
- Note: Embeddings are not supported in the current implementation as they require access to the Gemini Pro API

## Example Usage

### Chat Completion (curl)
```bash
# Using Gemini
curl -X POST "http://localhost:8000/api/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gemini-2.0-flash-lite",
       "provider": "gemini",
       "messages": [
         {
           "role": "user",
           "content": "Say hello!"
         }
       ]
     }'

# Using OpenAI
curl -X POST "http://localhost:8000/api/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gpt-3.5-turbo",
       "provider": "openai",
       "messages": [
         {
           "role": "user",
           "content": "Say hello!"
         }
       ]
     }'
```

### List Available Models
```bash
# List Gemini models
curl "http://localhost:8000/api/v1/models?provider=gemini"

# List OpenAI models
curl "http://localhost:8000/api/v1/models?provider=openai"
```

## API Endpoints

- `/api/v1/chat/completions` - Chat completions endpoint
- `/api/v1/embeddings` - Text embeddings endpoint (OpenAI only)
- `/api/v1/models` - List available models
- `/health` - Health check endpoint


## Running Tests
```bash
pytest tests/
```

## Adding More Providers 
- Implement a new service in `services/` inheriting from `BaseLLMService`
- Register it in the service factory
- Add your provider's API key and config to `.env` and `config.py`

## Requirements
See `requirements.txt` for all dependencies.

