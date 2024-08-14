import sys
import os
import logging
import azure.functions as func
from fastapi import FastAPI
from starlette.middleware.wsgi import WSGIMiddleware

# Add the app directory to the system path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "app"))
sys.path.insert(0, app_dir)

# Import the main FastAPI app
from app.main import app as fastapi_app

# Create a FastAPI application
app = FastAPI()

# Add the FastAPI application as a sub-application
app.mount("/", fastapi_app)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('FastAPI HTTP trigger function processed a request.')
    
    # Pass the request to FastAPI's WSGI middleware
    return func.WsgiMiddleware(app).handle(req, context)
