from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from .core import Base

class Document(Base):
    """
    Represents an uploaded document (PDF, TXT, etc.)
    """
    __tablename__ = 'documents'
    
    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    """
    Represents a chunk of a document, with its vector embedding.
    """
    __tablename__ = 'document_chunks'
    
    id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey('documents.id'), nullable=False)
    content = Column(String, nullable=False)
    # Gemini embeddings are typically 768 dimensions (for text-embedding-004)
    embedding = Column(Vector(768)) 
    chunk_index = Column(Integer, nullable=False)
    
    document = relationship("Document", back_populates="chunks")
