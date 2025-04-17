from fastapi.testclient import TestClient
from main import app  # assuming your FastAPI app is defined in main.py

client = TestClient(app)

def test_chat_completion_endpoint():
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "provider": "openai"
    }
    
    response = client.post("/api/v1/chat/completions", json=payload)
    # Check that the endpoint returns a successful status code and expected JSON structure
    assert response.status_code == 200
    data = response.json()
    assert "choices" in data  # or any other expected key in the response

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}  # Adjust based on your health check response

test_chat_completion_endpoint()