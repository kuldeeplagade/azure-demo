# exception_handlers.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "status": "failure",
            "status_code": exc.status_code,
            "data": None,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    validation_errors = exc.errors()   
    return JSONResponse(
        status_code=400,
        content={
            "message": "Validation error",
            "status": "failure",
            "status_code": 400,
            "data": validation_errors,
        },
    )


# Add an importable dictionary of exception handlers
exception_handlers = {
    StarletteHTTPException: http_exception_handler,
    RequestValidationError: validation_exception_handler,
}