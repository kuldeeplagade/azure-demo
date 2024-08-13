import logging
import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.main import app as fastapi_app  # Import your FastAPI app

# Create a middleware chain if needed
middleware = [
    Middleware(BaseHTTPMiddleware, dispatch=fastapi_app.middleware_stack),
    Middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]),
]

# Define the FastAPI app with the middleware chain
app = FastAPI(middleware=middleware)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Azure Function handler"""
    # Use FastAPI app to handle the request
    return func.AsgiFunctionHandler(app).handle(req, context)
