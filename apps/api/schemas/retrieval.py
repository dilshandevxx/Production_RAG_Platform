from pydantic import BaseModel, Field
from typing import List

class RetrievalRequest(BaseModel):
    query: str = Field(..., description="The user's question or search query")
    top_k: int = Field(default=3, description="The number of relevant chunks to retrieve")

class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int

class RetrievalResponse(BaseModel):
    query: str
    results: List[RetrievedChunk]
