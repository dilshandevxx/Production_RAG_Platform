# Production RAG Platform 🚀

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)

An industry-grade, highly scalable Retrieval-Augmented Generation (RAG) platform built with Python, FastAPI, and PostgreSQL (`pgvector`). This platform allows you to securely ingest private documents, convert them into mathematical vector embeddings using Google Gemini, and perform semantic vector searches to power an intelligent, context-aware AI chatbot.

## 🏗 Architecture

The platform is designed using a **modular, domain-driven architecture** ensuring scalability, testability, and separation of concerns.

- **Apps (`apps/api/`)**: Contains the FastAPI entrypoint, HTTP routers, and Pydantic schemas. It acts strictly as the transport layer.
- **Services (`services/`)**: Contains the core business logic (Ingestion, Retrieval, Chat orchestration). Services are decoupled from the HTTP layer.
- **Packages (`packages/`)**: Standalone internal libraries (Database management, LLM integrations, Vector Embeddings).

## ✨ Features

- **Document Ingestion**: Automatically chunk large texts and generate 768-dimensional vector embeddings.
- **Semantic Vector Search**: Utilizes `pgvector` for lightning-fast L2 distance mathematical similarity searches.
- **Streaming LLM Responses**: Real-time server-sent events (SSE) streaming of AI responses using `gemini-2.5-flash`.
- **Asynchronous by Default**: Built entirely on `asyncio`, utilizing `asyncpg` for non-blocking database transactions.
- **Dockerized Infrastructure**: Complete local development environment bundled via `docker-compose` (PostgreSQL + Redis).
- **Database Migrations**: Fully managed schema versioning using `Alembic`.

## 🛠 Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [`pgvector`](https://github.com/pgvector/pgvector)
- **ORM & Migrations**: [SQLAlchemy 2.0 (Async)](https://www.sqlalchemy.org/) & [Alembic](https://alembic.sqlalchemy.org/)
- **AI / LLM**: [Google GenAI SDK](https://github.com/google/genai-python) (`gemini-2.5-flash`, `gemini-embedding-2`)
- **Infrastructure**: Docker & Docker Compose

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- A Google Gemini API Key

### 1. Clone & Setup Environment
```bash
git clone <your-repo-url>
cd production-rag-platform

# Create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows
# source .venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/rag_db
```

### 3. Start Infrastructure & Migrate Database
```bash
# Start PostgreSQL and Redis in the background
docker-compose up -d

# Run Alembic migrations to create the pgvector tables
alembic upgrade head
```

### 4. Run the API Server
```bash
# Start the FastAPI server in development mode
fastapi dev apps/api/main.py
```
Your API will now be available at: **http://127.0.0.1:8000**
Swagger Interactive Docs: **http://127.0.0.1:8000/docs**

---

## 📡 API Endpoints

### `POST /ingest/`
Upload and vectorize a document.
```json
{
  "filename": "company-policy.txt",
  "content": "Employees get 20 days of paid time off per year."
}
```

### `POST /retrieve/`
Perform a vector similarity search across all ingested documents.
```json
{
  "query": "How many days off do I get?",
  "top_k": 3
}
```

### `POST /chat/stream`
Chat with the AI using your ingested documents as context (Streams response).
```bash
curl -N -X 'POST' \
  'http://127.0.0.1:8000/chat/stream' \
  -H 'Content-Type: application/json' \
  -d '{ "query": "How many days off do I get?" }'
```

---

## 📁 Directory Structure

```text
production-rag-platform/
├── apps/
│   └── api/                # FastAPI Application (Routers, Schemas, Main)
├── packages/
│   ├── database/           # SQLAlchemy Models & Alembic Migrations
│   ├── embeddings/         # Gemini Vector Embedding Logic
│   └── llm/                # Gemini Text Generation Logic
├── services/
│   ├── ingestion/          # Document Chunking & Saving Logic
│   ├── retrieval/          # pgvector Similarity Search Logic
│   └── chat/               # RAG Orchestration & Streaming
├── docs/                   # Architecture Decisions (ADRs) & Progress
├── docker-compose.yml      # Local Infrastructure
├── alembic.ini             # Migration Config
└── requirements.txt        # Python Dependencies
```
