import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from packages.database import Document, DocumentChunk
from packages.embeddings import EmbeddingsProvider

class IngestionService:
    """
    Handles the ingestion of documents into the RAG platform.
    This includes chunking the text, generating embeddings, and saving to the DB.
    """
    def __init__(self, db_session: AsyncSession, embeddings_provider: EmbeddingsProvider):
        self.db = db_session
        self.embeddings_provider = embeddings_provider

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Splits a large text into smaller overlapping chunks.
        (A simple character-based chunker for demonstration. In production, 
        you might use LangChain's RecursiveCharacterTextSplitter).
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunks.append(text[start:end])
            if end == text_length:
                break
            start += chunk_size - overlap
            
        return chunks

    async def ingest_text(self, filename: str, content: str) -> str:
        """
        Ingests a raw text string, chunks it, embeds it, and saves it to Postgres.
        Returns the generated Document ID.
        """
        # 1. Create a new Document record
        doc_id = str(uuid.uuid4())
        document = Document(
            id=doc_id,
            filename=filename,
            metadata_json={"source": "upload"}
        )
        self.db.add(document)
        
        # 2. Chunk the text
        text_chunks = self.chunk_text(content)
        if not text_chunks:
            await self.db.commit()
            return doc_id
            
        # 3. Generate embeddings for all chunks in bulk
        embeddings = await self.embeddings_provider.embed_texts(text_chunks)
        
        # 4. Save chunks and embeddings to the database
        for i, (chunk_text, embedding) in enumerate(zip(text_chunks, embeddings)):
            chunk_record = DocumentChunk(
                id=str(uuid.uuid4()),
                document_id=doc_id,
                content=chunk_text,
                embedding=embedding,
                chunk_index=i
            )
            self.db.add(chunk_record)
            
        # 5. Commit the transaction
        await self.db.commit()
        return doc_id
