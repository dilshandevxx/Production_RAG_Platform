from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from packages.llm import LLMProvider
from services.retrieval.core import RetrievalService

class ChatService:
    """
    Orchestrates the entire RAG pipeline:
    1. Retrieves relevant context from the database based on the user's question.
    2. Constructs a prompt including both the context and the question.
    3. Streams the response from the LLM back to the user.
    """
    def __init__(self, retrieval_service: RetrievalService, llm_provider: LLMProvider):
        self.retrieval_service = retrieval_service
        self.llm_provider = llm_provider

    async def chat_stream(self, query: str) -> AsyncGenerator[str, None]:
        """
        Retrieves context and streams the LLM's response.
        """
        # 1. Retrieve the most relevant chunks from PostgreSQL
        results = await self.retrieval_service.search(query, top_k=3)
        
        # 2. Extract just the text content from the results
        context_texts = [result["content"] for result in results]
        
        # 3. Combine them into a single string
        context_block = "\n\n---\n\n".join(context_texts)
        
        # 4. Construct the powerful RAG prompt
        system_prompt = f"""
        You are an intelligent, helpful AI assistant.
        You must answer the user's question using ONLY the context provided below.
        If the context does not contain the answer, simply say "I don't have enough information to answer that based on the provided documents."
        Do NOT make up an answer.
        
        CONTEXT:
        {context_block}
        """
        
        # 5. Stream the response directly from Google Gemini
        async for chunk in self.llm_provider.generate_stream(prompt=query, system_prompt=system_prompt):
            yield chunk
