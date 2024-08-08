from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.utils.logger import logger  # Import your custom logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Route called: {request.url.path} - Method: {request.method}")
        # logger.info(f"{request.method} Method for route: '{request.url.path}'")   # just for or log message 
        response = await call_next(request)
        return response
        