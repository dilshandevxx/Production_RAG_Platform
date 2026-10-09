from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from packages.database import get_db_session
from packages.embeddings import GeminiEmbeddingsProvider
from services.ingestion import IngestionService
from ..schemas.ingest import IngestRequest, IngestResponse

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

# Dependency to get the embeddings provider
def get_embeddings_provider():
    return GeminiEmbeddingsProvider()

@router.post("/", response_model=IngestResponse)
async def ingest_document(
    request: IngestRequest,
    db_session: AsyncSession = Depends(get_db_session),
    embeddings_provider: GeminiEmbeddingsProvider = Depends(get_embeddings_provider)
):
    """
    Ingest a document by chunking its content, generating vector embeddings, 
    and storing them in the PostgreSQL database.
    """
    service = IngestionService(db_session, embeddings_provider)
    
    doc_id = await service.ingest_text(
        filename=request.filename,
        content=request.content
    )
    
    return IngestResponse(document_id=doc_id)
