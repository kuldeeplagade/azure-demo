import logging
import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.main import app as fastapi_app  # Import the FastAPI app

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Convert the Azure Function HTTP request to a FastAPI request
    asgi_handler = func.AsgiMiddleware(fastapi_app)
    response = await asgi_handler.handle_async(req, context)
    
    return response
