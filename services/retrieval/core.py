from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from packages.database import DocumentChunk
from packages.embeddings import EmbeddingsProvider

class RetrievalService:
    """
    Handles searching the database for document chunks that are most relevant 
    to a user's question using vector similarity.
    """
    def __init__(self, db_session: AsyncSession, embeddings_provider: EmbeddingsProvider):
        self.db = db_session
        self.embeddings_provider = embeddings_provider

    async def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Takes a question, converts it to an embedding, and finds the closest chunks in the database.
        """
        # 1. Convert the user's question into mathematical numbers (an embedding)
        query_embedding = await self.embeddings_provider.embed_query(query)
        
        # 2. Ask PostgreSQL to find the chunks with embeddings closest to our question's embedding
        # We use the L2 distance operator (<->) provided by pgvector
        stmt = (
            select(DocumentChunk)
            .order_by(DocumentChunk.embedding.l2_distance(query_embedding))
            .limit(top_k)
        )
        
        result = await self.db.execute(stmt)
        chunks = result.scalars().all()
        
        # 3. Return the results
        return [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "content": chunk.content,
                "chunk_index": chunk.chunk_index
            }
            for chunk in chunks
        ]
