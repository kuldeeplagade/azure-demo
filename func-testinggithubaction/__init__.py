import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Change to specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods. Change to specific methods if needed.
    allow_headers=["*"],  # Allow all headers. Change to specific headers if needed.
)

# Import routes here
from app.routes import user_route

# Include routes
app.include_router(user_route.router)
