"""
FastAPI application entrypoint.
Based on db-chat-nl architecture.md:13-20 (Backend structure)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routes


# Initialize FastAPI app
app = FastAPI(
    title="Generated Chat API",
    version="0.1.0",
    description="AI-powered chat interface with database integration"
)

# Configure CORS
# Based on tech.md:125-126 (CORS for production domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
# Based on modules.md:7-12 (API routes structure)
app.include_router(routes.router)

# Legacy health endpoint for backward compatibility
@app.get("/health")
def health():
    """Root health check endpoint."""
    return {"status": "ok", "service": "chat-api"}


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "service": "Generated Chat API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


# TODO: Wire real services with dependency injection
# Based on modules.md:50-108 (Service layer)
# Example:
# from .services.chat import ChatService
# from .services.database import DatabaseService
# from .services.llm import LLMService
#
# @app.on_event("startup")
# async def startup_event():
#     # Initialize services
#     database_service = DatabaseService(...)
#     llm_service = LLMService(api_key=settings.ANTHROPIC_API_KEY)
#     chat_service = ChatService(database_service, llm_service)
#     # Store in app state for dependency injection
