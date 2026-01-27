"""
API routes for chat functionality.
Based on db-chat-nl modules.md:7-12 (SSE streaming endpoint)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator, Optional
import json
import asyncio
from ..services.chat import ChatService
from ..services.database import DatabaseService, DatabaseServiceStub
from ..services.llm import LLMService


router = APIRouter(prefix="/api/v1", tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request schema."""
    message: str
    conversation_id: Optional[str] = None


async def stream_chat_response(
    user_message: str,
    chat_service: ChatService
) -> AsyncGenerator[str, None]:
    """
    Generate SSE stream for chat response.
    Based on db-chat-nl architecture.md:96 (SSE streaming pattern)

    Implements heartbeat mechanism to prevent timeout (tech.md:63-64).

    Args:
        user_message: User's question
        chat_service: Chat service instance

    Yields:
        SSE formatted messages
    """
    try:
        # Send initial connection confirmation
        yield f"data: {json.dumps({'type': 'connected'})}\n\n"

        # TODO: Implement full streaming logic with heartbeat
        # Based on modules.md:100-108 (chat orchestration)
        # 1. Load database schema
        # 2. Retrieve learned queries
        # 3. Construct prompt with examples
        # 4. Stream LLM response with SSE
        # 5. Send heartbeat every 10s to prevent timeout

        # Stub: Send a simple response
        response_data = chat_service.process_message(user_message)

        yield f"data: {json.dumps({'type': 'message', 'content': response_data['response']})}\n\n"

        if response_data.get('sql'):
            yield f"data: {json.dumps({'type': 'sql', 'query': response_data['sql']})}\n\n"

        if response_data.get('results'):
            yield f"data: {json.dumps({'type': 'results', 'data': response_data['results']})}\n\n"

        # Send completion event
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    except Exception as e:
        error_data = {
            'type': 'error',
            'message': str(e)
        }
        yield f"data: {json.dumps(error_data)}\n\n"


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    SSE streaming chat endpoint.
    Based on db-chat-nl modules.md:9 (POST /api/v1/chat/stream)

    Streams AI responses in real-time using Server-Sent Events.

    Args:
        request: Chat request with user message

    Returns:
        StreamingResponse with SSE events
    """
    # TODO: Replace stubs with real service instances from dependency injection
    database_service = DatabaseServiceStub()
    llm_service = LLMService()
    chat_service = ChatService(database_service, llm_service)

    return StreamingResponse(
        stream_chat_response(request.message, chat_service),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    Based on modules.md:10
    """
    return {
        "status": "ok",
        "service": "chat-api",
        "version": "0.1.0"
    }


@router.get("/database/schema")
async def get_database_schema():
    """
    Get database schema information.
    Based on modules.md:11

    Returns:
        Database schema with tables and columns
    """
    # TODO: Inject real database service
    database_service = DatabaseServiceStub()

    try:
        schema = database_service.get_schema()
        return {"schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
