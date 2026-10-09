from pydantic import BaseModel, Field

class IngestRequest(BaseModel):
    filename: str = Field(..., description="The name of the file being ingested")
    content: str = Field(..., description="The raw text content of the document")

class IngestResponse(BaseModel):
    document_id: str = Field(..., description="The unique ID of the ingested document")
    status: str = Field(default="success", description="Status of the ingestion process")
