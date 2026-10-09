from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's chat question")
