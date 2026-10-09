from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from packages.database import get_db_session
from packages.embeddings import GeminiEmbeddingsProvider
from packages.llm import GeminiProvider
from services.retrieval import RetrievalService
from services.chat import ChatService
from ..schemas.chat import ChatRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

def get_embeddings_provider():
    return GeminiEmbeddingsProvider()

def get_llm_provider():
    return GeminiProvider()

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    db_session: AsyncSession = Depends(get_db_session),
    embeddings_provider: GeminiEmbeddingsProvider = Depends(get_embeddings_provider),
    llm_provider: GeminiProvider = Depends(get_llm_provider)
):
    """
    Takes a user question, searches the database for relevant context, 
    and streams back an AI-generated answer.
    """
    retrieval_service = RetrievalService(db_session, embeddings_provider)
    chat_service = ChatService(retrieval_service, llm_provider)
    
    # Return a Server-Sent Events (SSE) stream or just a raw text stream
    return StreamingResponse(
        chat_service.chat_stream(request.query),
        media_type="text/event-stream"
    )
