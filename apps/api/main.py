from dotenv import load_dotenv
load_dotenv()  # This explicitly forces Python to read your .env file!

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import ingest, retrieval, chat

app = FastAPI(
    title="Production RAG API",
    description="API for ingesting documents and chatting with the RAG platform",
    version="0.1.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ingest.router)
app.include_router(retrieval.router)
app.include_router(chat.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
