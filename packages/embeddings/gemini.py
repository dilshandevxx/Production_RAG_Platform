import os
from typing import List, Optional
from google import genai
from google.genai import types

class GeminiEmbeddingsProvider:
    """
    Implementation of the EmbeddingsProvider interface for Google's Gemini models
    using the official google-genai SDK.
    """
    
    def __init__(self, api_key: Optional[str] = None, default_model: str = "gemini-embedding-2"):
        # Use provided key, or fallback to environment variable
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key or key == "your_key_here":
            raise ValueError("GEMINI_API_KEY is not set. Please set it in your .env file.")
            
        self.client = genai.Client(api_key=key)
        self.default_model = default_model

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of texts using Gemini's embedding model.
        Usually used for embedding documents being ingested.
        """
        if not texts:
            return []
            
        # The new SDK supports batch embedding
        # We specify task_type="RETRIEVAL_DOCUMENT" for text being indexed
        response = await self.client.aio.models.embed_content(
            model=self.default_model,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=768
            )
        )
        
        # response.embeddings is a list of embeddings
        return [emb.values for emb in response.embeddings]
        
    async def embed_query(self, query: str) -> List[float]:
        """
        Embeds a single search query.
        We specify task_type="RETRIEVAL_QUERY" to optimize the embedding for searching.
        """
        response = await self.client.aio.models.embed_content(
            model=self.default_model,
            contents=query,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=768
            )
        )
        
        return response.embeddings[0].values
