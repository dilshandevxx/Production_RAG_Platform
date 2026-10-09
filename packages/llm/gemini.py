import os
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types

class GeminiProvider:
    """
    Implementation of the LLMProvider interface for Google's Gemini models
    using the official google-genai SDK.
    """
    
    def __init__(self, api_key: Optional[str] = None, default_model: str = "gemini-2.5-flash"):
        # Use provided key, or fallback to environment variable
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key or key == "your_key_here":
            raise ValueError("GEMINI_API_KEY is not set. Please set it in your .env file.")
            
        self.client = genai.Client(api_key=key)
        self.default_model = default_model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generates a text response from Gemini.
        Note: The google-genai SDK currently expects a single prompt string or an array of contents.
        We map standard role-based messages (user/assistant/system) to Gemini's format.
        """
        target_model = model or self.default_model
        
        # Convert standard dict messages into Gemini Content objects
        contents = []
        system_instruction = None
        
        for msg in messages:
            role = msg.get("role", "user")
            text = msg.get("content", "")
            
            if role == "system":
                # Gemini handles system instructions separately in config
                system_instruction = text
            else:
                # Map 'assistant' to 'model', everything else to 'user'
                gemini_role = "model" if role == "assistant" else "user"
                contents.append(
                    types.Content(role=gemini_role, parts=[types.Part.from_text(text=text)])
                )
                
        # Configure generation parameters
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        if system_instruction:
            config.system_instruction = system_instruction
            
        # Call the API asynchronously
        response = await self.client.aio.models.generate_content(
            model=target_model,
            contents=contents,
            config=config
        )
        
        return response.text

    async def generate_stream(self, prompt: str, system_prompt: Optional[str] = None) -> Any:
        """
        Streams a text response from Gemini.
        """
        config = types.GenerateContentConfig()
        if system_prompt:
            config.system_instruction = system_prompt
            
        # The new SDK provides generate_content_stream
        response_stream = await self.client.aio.models.generate_content_stream(
            model=self.default_model,
            contents=prompt,
            config=config
        )
        
        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text
