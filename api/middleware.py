import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", "unknown")
        start_time = time.time()
        logger.info(f"Request {request_id}: {request.method} {request.url.path}")
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Response {request_id}: {response.status_code} in {process_time:.4f}s")
        response.headers["X-Process-Time"] = str(process_time)
        return response
