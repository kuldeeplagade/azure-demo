import sys
import os
import logging
import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import engine
from app.routes import user_route
from app.database.middleware import LoggingMiddleware
from app.models import models
from app.exceptions.exception_handlers import exception_handlers

# Add the app directory to the system path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app"))
sys.path.insert(0, app_dir)

# Print statements to debug path issues
print("App directory:", app_dir)
print("Sys path:", sys.path)

# Create the FastAPI application
app = FastAPI()

# Set up database models
models.Base.metadata.create_all(bind=engine)

# Add middleware
app.add_middleware(LoggingMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers
for exc_class, handler in exception_handlers.items():
    app.add_exception_handler(exc_class, handler)

# Include routes
app.include_router(user_route.router)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('FastAPI HTTP trigger function processed a request.')
    
    # Pass the request to FastAPI's WSGI middleware
    return func.WsgiMiddleware(app).handle(req, context)
