import logging
import azure.functions as func
from mangum import Mangum
from app.main import app  # Import your FastAPI app

# Wrap the FastAPI app with Mangum to handle requests in a serverless environment
handler = Mangum(app)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Use the Mangum handler to process the incoming HTTP request
    return func.AsgiFunctionHandler(handler).handle(req, context)
