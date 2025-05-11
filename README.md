# LLM Gateway API

A unified API gateway for multiple Large Language Model (LLM) providers. This project allows you to interact with different LLM APIs (currently OpenAI, but easily extendable) through a single, standardized REST API.

## Features
- Unified API for chat completions, text embeddings, and model info
- Standardized request/response formats
- Easy provider switching (OpenAI, Anthropic, Groq, etc.)
- Built with FastAPI (async, high performance)
- Ready for extension and production use

## How It Works
- The API exposes endpoints for chat completions, embeddings, and model info
- Each provider is implemented as a service class
- The API routes requests to the correct provider based on your request or configuration
- Responses are normalized to a common schema

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
DEFAULT_PROVIDER=openai
ENABLE_CACHE=false
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

### 5. Access the API docs
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser for the interactive Swagger UI.

## Example Usage

### Chat Completion (curl)
```bash
curl -X POST "http://localhost:8000/api/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "gpt-3.5-turbo",
           "messages": [
             {"role": "user", "content": "Hello!"}
           ]
         }'
```

### Embeddings (curl)
```bash
curl -X POST "http://localhost:8000/api/v1/embeddings" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "text-embedding-ada-002",
           "input": "Hello, world!"
         }'
```

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

## Contributing
Pull requests and issues are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

---

**Note:** This project is for educational and prototyping purposes. Do not expose your API keys in production. Always secure your endpoints and secrets. 