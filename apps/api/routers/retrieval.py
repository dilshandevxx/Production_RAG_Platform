from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from packages.database import get_db_session
from packages.embeddings import GeminiEmbeddingsProvider
from services.retrieval import RetrievalService
from ..schemas.retrieval import RetrievalRequest, RetrievalResponse

router = APIRouter(prefix="/retrieve", tags=["Retrieval"])

def get_embeddings_provider():
    return GeminiEmbeddingsProvider()

@router.post("/", response_model=RetrievalResponse)
async def retrieve_documents(
    request: RetrievalRequest,
    db_session: AsyncSession = Depends(get_db_session),
    embeddings_provider: GeminiEmbeddingsProvider = Depends(get_embeddings_provider)
):
    """
    Takes a user query, generates an embedding, and retrieves the most relevant 
    document chunks from the database using vector search.
    """
    service = RetrievalService(db_session, embeddings_provider)
    
    results = await service.search(
        query=request.query,
        top_k=request.top_k
    )
    
    return RetrievalResponse(
        query=request.query,
        results=results
    )
