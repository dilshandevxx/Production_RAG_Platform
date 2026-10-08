# Production RAG Platform

> A production-grade Retrieval-Augmented Generation platform demonstrating end-to-end
> AI systems engineering — from document ingestion and hybrid retrieval to evaluation,
> security, observability, cloud deployment and scalability.

---

## What This Project Demonstrates

This is not a chatbot demo. It is an engineering portfolio showing:

| Competency | What's Built |
|---|---|
| **RAG internals** | Custom chunking strategies, hybrid retrieval (semantic + keyword), reranking, citation mapping |
| **Backend engineering** | FastAPI, async processing, Pydantic validation, typed interfaces |
| **Data engineering** | PostgreSQL schema design, pgvector indexes, Alembic migrations |
| **Async systems** | Async ingestion worker, job queue, retries with exponential backoff, idempotency |
| **Security** | Multi-tenancy, RBAC, prompt injection defenses, API key hashing, audit logging |
| **Evaluation** | Retrieval metrics (Recall@K, MRR, NDCG), generation metrics (Faithfulness, Citation accuracy) |
| **Observability** | OpenTelemetry traces, Prometheus metrics, Grafana dashboards, structured logs |
| **Reliability** | Graceful failure, dependency degradation, failure scenario testing |
| **DevOps** | Docker, CI/CD (GitHub Actions), Terraform, AWS deployment |
| **Cost engineering** | Token tracking per request/tenant, cache savings measurement |

---

## Architecture

```
Client
  │
  ▼
API Gateway / Reverse Proxy
  │
  ▼
FastAPI Application (apps/api/)
  ├── Auth & RBAC
  ├── Document Service
  ├── RAG Query Engine
  ├── Evaluation Service
  └── Usage/Analytics
  │
  ├──► PostgreSQL + pgvector  (metadata, chunks, vectors)
  ├──► Redis                  (cache, rate limiting, job queue)
  ├──► S3 / MinIO             (original document files)
  └──► LLM / Embedding APIs   (OpenAI, Anthropic, Cohere)
  │
  ▼
Ingestion Worker (services/worker/)
  └── Parse → Clean → Chunk → Embed → Index
```

**Architecture Decision Records** — explaining every major design choice:
- [ADR-001: Why Python + FastAPI?](docs/adr/ADR-001-python-fastapi.md)
- [ADR-002: Why PostgreSQL + pgvector?](docs/adr/ADR-002-postgresql-pgvector.md) *(Phase 2)*
- [ADR-003: Why hybrid retrieval?](docs/adr/ADR-003-hybrid-retrieval.md) *(Phase 5)*
- [ADR-004: Why asynchronous ingestion?](docs/adr/ADR-004-async-ingestion.md) *(Phase 4)*
- [ADR-005: Why Redis?](docs/adr/ADR-005-redis.md) *(Phase 4)*

---

## Technology Stack

| Layer | Technology | Why |
|---|---|---|
| Backend | Python 3.12 + FastAPI | Async-native, Pydantic validation, AI ecosystem |
| Database | PostgreSQL 16 + pgvector | Relational + vector in one system; avoids extra infra |
| Cache/Queue | Redis 7 | Caching, rate limiting, job queue |
| Object Storage | S3 / MinIO (local) | Large files off the DB; S3-compatible API |
| LLM | OpenAI GPT-4o-mini (default) | Cost-effective; swappable via provider abstraction |
| Embeddings | OpenAI text-embedding-3-small | Strong quality/cost ratio; 1536-dim vectors |
| Reranking | Cohere Rerank | Cross-encoder quality; API-based, no GPU needed |
| Tracing | OpenTelemetry → Jaeger | Industry standard; per-stage latency visibility |
| Metrics | Prometheus + Grafana | Standard production monitoring stack |
| CI/CD | GitHub Actions | Free for public repos; YAML-based, reproducible |
| IaC | Terraform | Reproducible cloud infrastructure |
| Cloud | AWS | RDS, S3, ECS/EC2, IAM |

---

## Project Structure

```
production-rag-platform/
├── apps/
│   ├── api/              ← FastAPI application
│   └── web/              ← Next.js frontend (Phase 35)
├── services/
│   ├── ingestion/        ← Document parsing and chunking logic
│   ├── retrieval/        ← Hybrid search and reranking
│   ├── evaluation/       ← Retrieval/generation metrics
│   └── worker/           ← Async ingestion worker process
├── packages/
│   ├── rag/              ← Core RAG pipeline (chunking, embedding, generation)
│   ├── embeddings/       ← Embedding provider abstraction
│   ├── llm/              ← LLM provider abstraction
│   ├── database/         ← SQLAlchemy models, repositories, migrations
│   └── observability/    ← OpenTelemetry, Prometheus, structured logging
├── infrastructure/
│   ├── docker/           ← Docker Compose + config files
│   ├── terraform/        ← AWS infrastructure as code
│   └── kubernetes/       ← K8s manifests (Phase 30 if justified)
├── evaluations/
│   ├── datasets/         ← Evaluation question sets
│   ├── experiments/      ← Experiment configuration and results
│   └── benchmarks/       ← Benchmark reports
├── tests/
│   ├── unit/             ← Fast, no external dependencies
│   ├── integration/      ← Requires DB + Redis
│   ├── security/         ← Tenant isolation, RBAC, prompt injection
│   └── rag/              ← RAG quality assertions
├── docs/
│   ├── adr/              ← Architecture Decision Records
│   ├── architecture/     ← System diagrams
│   ├── threat-model/     ← Security threat model
│   └── runbooks/         ← Operational procedures
└── .github/
    └── workflows/        ← CI/CD pipelines
```

---

## Quick Start (Local Development)

### Prerequisites
- Python 3.12+
- Docker Desktop
- Git

### Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd production-rag-platform

# 2. Install Python dependencies
make install

# 3. Install pre-commit hooks (runs quality checks before every commit)
make hooks

# 4. Copy environment template and fill in your API keys
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY at minimum

# 5. Start local infrastructure
make infra-up

# 6. Apply database migrations
make migrate
```

### Services after `make infra-up`

| Service | URL | Credentials |
|---|---|---|
| PostgreSQL | `localhost:5432` | `rag_user` / `rag_password` |
| Redis | `localhost:6379` | — |
| MinIO (S3) UI | http://localhost:9001 | `minioadmin` / `minioadmin` |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3001 | `admin` / `admin` |
| Jaeger (Traces) | http://localhost:16686 | — |

---

## Development Phases

| Phase | Focus | Status |
|---|---|---|
| 0 | Foundation & Environment | ✅ Complete |
| 1 | RAG Core (Prototype) | 🔲 Next |
| 2 | Data Layer (PostgreSQL + pgvector) | 🔲 |
| 3 | API Layer (FastAPI) | 🔲 |
| 4 | Async Ingestion Pipeline | 🔲 |
| 5 | Hybrid Retrieval + Reranking | 🔲 |
| 6 | Evaluation Framework | 🔲 |
| 7 | Security & Multi-Tenancy | 🔲 |
| 8 | Observability | 🔲 |
| 9 | Reliability Engineering | 🔲 |
| 10 | Cloud & DevOps | 🔲 |
| 11 | Performance & Cost | 🔲 |
| 12 | Portfolio Finalization | 🔲 |

---

## Engineering Principles

1. **Understand before using** — explain WHY before HOW
2. **Simplicity before complexity** — add infrastructure only when requirements justify it
3. **Measure before optimizing** — profile before changing performance-critical code
4. **Design for failure** — every external call has timeouts, retries, and fallbacks
5. **Security is structural** — multi-tenancy and RBAC are core invariants, not add-ons
6. **Evaluation is engineering** — retrieval and generation quality are measured with metrics

---

## Limitations (Honest Assessment)

> *"Do not claim million-user scale simply because the architecture could theoretically scale."*

- **Scale**: Designed and tested for development and demo workloads. Production sizing requires load testing.
- **LLM cost**: Token costs scale linearly. Cost per query depends on document size and model chosen.
- **Evaluation dataset**: Synthetic/manually curated. Real-world performance may differ.
- **Reranker**: Uses external API (Cohere). For low-latency production, a local cross-encoder would be needed.

---

*Built as an AI/ML engineering portfolio project demonstrating end-to-end AI systems engineering.*
