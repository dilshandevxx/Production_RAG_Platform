from typing import Protocol, List

class EmbeddingsProvider(Protocol):
    """
    Base interface for all Embedding providers (OpenAI, Anthropic, Gemini, etc.).
    """
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Converts a list of text strings into a list of vector embeddings.
        
        Args:
            texts: A list of strings to embed.
            
        Returns:
            A list where each item is a list of floats representing the vector.
        """
        ...
        
    async def embed_query(self, query: str) -> List[float]:
        """
        Converts a single search query into a vector embedding.
        Providers sometimes use different embedding models/parameters for queries vs documents.
        
        Args:
            query: The search query string.
            
        Returns:
            A single list of floats representing the vector.
        """
        ...
