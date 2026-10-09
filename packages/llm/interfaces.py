from typing import Protocol, List, Dict, Any, Optional

class LLMProvider(Protocol):
    """
    Base interface for all Language Model providers (OpenAI, Anthropic, Gemini, etc.).
    By programming against this protocol, the rest of the application remains agnostic
    to which specific LLM is actually being used.
    """
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generates a text response from the LLM based on a list of chat messages.
        
        Args:
            messages: A list of message dicts with 'role' (user, assistant, system) and 'content'.
            model: The specific model ID to use. If None, uses the provider's default.
            temperature: Sampling temperature (0.0 to 1.0).
            max_tokens: Maximum number of tokens to generate.
            
        Returns:
            The text response from the assistant.
        """
        ...
