from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import engine
from app.routes import user_route
from app.database.middleware import LoggingMiddleware
from app.models import models
from app.exceptions.exception_handlers import exception_handlers


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

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

# Include router
app.include_router(user_route.router)


