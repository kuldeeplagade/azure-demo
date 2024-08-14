import logging
from azure.functions import HttpRequest, HttpResponse
from app.main import app
from fastapi import Request
from starlette.responses import Response
from starlette.types import Scope, Receive, Send

class AsgiToAzureFunction:
    def __init__(self, app):
        self.app = app

    async def __call__(self, req: HttpRequest, context) -> HttpResponse:
        asgi_req = self._convert_to_asgi(req)
        response = Response()
        await self.app(asgi_req, asgi_req.receive, response.send)
        return self._convert_to_azure_response(response)

    def _convert_to_asgi(self, req: HttpRequest) -> Request:
        scope = {
            "type": "http",
            "method": req.method,
            "path": req.route_params.get("route", "/"),
            "query_string": req.url.query.encode(),
            "headers": [(k.encode(), v.encode()) for k, v in req.headers.items()],
        }
        return Request(scope, receive=self._receive(req))

    def _receive(self, req: HttpRequest):
        async def receive() -> Receive:
            return {"type": "http.request", "body": req.get_body(), "more_body": False}

        return receive

    def _convert_to_azure_response(self, response: Response) -> HttpResponse:
        return HttpResponse(
            body=response.body,
            status_code=response.status_code,
            headers=dict(response.headers),
            mimetype=response.media_type,
        )

handler = AsgiToAzureFunction(app)

def main(req: HttpRequest, context) -> HttpResponse:
    logging.info('Processing request with FastAPI in Azure Functions.')
    return handler(req, context)
