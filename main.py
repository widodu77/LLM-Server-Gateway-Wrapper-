from fastapi import FastAPI
from api.routers import chat, embeddings, models

app = FastAPI(
    title="LLM Gateway API",
    description="A unified API gateway for multiple LLM providers",
    version="1.0.0"
)

# Include the Chat Completions router
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat Completions"])

# Include the Text Embeddings router
app.include_router(embeddings.router, prefix="/api/v1/embeddings", tags=["Text Embeddings"])

# Include the Model Information router
app.include_router(models.router, prefix="/api/v1/models", tags=["Model Information"])

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}
