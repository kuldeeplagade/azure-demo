import logging
import azure.functions as func
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import user_route
from app.database.db import engine
from app.models import models
from app.exceptions.exception_handlers import exception_handlers
from app.database.middleware import LoggingMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    
    try:
        # Pass the request to FastAPI's WSGI middleware
        return func.WsgiMiddleware(app).handle(req, context)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
