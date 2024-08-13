import logging
import azure.functions as func  # Correct import for Azure Functions
from fastapi import FastAPI
from azure.functions import AsgiMiddleware
from app.main import app  # Import your FastAPI app

# Initialize the FastAPI app
fastapi_app = app

# Entry point for the Azure Function
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Wrap the FastAPI app with AsgiMiddleware for Azure Functions
    return AsgiMiddleware(fastapi_app).handle(req, context)
