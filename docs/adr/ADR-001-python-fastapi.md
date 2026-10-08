# ADR-001: Why Python + FastAPI for the Backend?

**Status:** Accepted
**Date:** 2026-10-08
**Author:** Dilshan

---

## Context

We need a backend web framework to build the REST API for the Production RAG Platform.
The platform serves AI workloads: it calls LLM APIs, embedding APIs, and performs
vector database queries — all of which are I/O-bound and benefit from async execution.

The framework choice determines developer experience, API documentation quality,
runtime performance under concurrency, and ecosystem compatibility with AI libraries.

---

## Decision

**Use Python 3.12 + FastAPI** as the backend framework.

---

## Alternatives Considered

| Alternative | Reason Not Chosen |
|---|---|
| **Flask** | No native async support; no automatic request validation; no built-in OpenAPI docs |
| **Django** | Full-stack ORM + templates overhead we don't need; async support added late; heavier |
| **Django REST Framework** | Same Django overhead; not async-first |
| **Node.js + Express** | Python AI ecosystem (LangChain, sentence-transformers, numpy) is far richer; team skill |
| **Go + Gin** | Excellent performance but no AI library ecosystem; much harder to call Python ML code |
| **Rust + Axum** | Strongest performance, but extreme development overhead for AI prototype |

---

## Why FastAPI Specifically

1. **Async-native:** Built on Starlette + asyncio. Every route can be `async def`.
   This matters because most operations (LLM calls, DB queries, S3 calls) are I/O-bound —
   async lets one process serve many concurrent requests while waiting for external I/O.

2. **Pydantic validation:** Request bodies are automatically validated against Pydantic schemas.
   Invalid input is rejected before it reaches business logic. No manual validation code.

3. **Automatic OpenAPI docs:** FastAPI generates `/docs` (Swagger UI) and `/redoc` automatically
   from type annotations. The API is self-documenting with zero extra work.

4. **Type annotations:** FastAPI's design encourages typed interfaces, which makes
   `mypy` static analysis effective and reduces runtime bugs.

5. **Python AI ecosystem:** `openai`, `anthropic`, `sentence-transformers`, `langchain`,
   `numpy`, `ragas` — all Python. The backend shares the same language as AI tooling.

6. **Production adoption:** Uber, Netflix, Microsoft, and many others use FastAPI in production.
   It is not experimental.

---

## Trade-offs Accepted

| Trade-off | Mitigation |
|---|---|
| **Python GIL limits CPU parallelism** | Our workload is I/O-bound (LLM/DB calls), not CPU-bound. CPU-heavy work (if any) goes to separate processes or workers. |
| **Python is slower than Go/Rust** | The bottleneck will be LLM API latency (200–2000ms), not Python overhead (1–5ms). Premature performance optimization here would be wrong. |
| **Less opinionated than Django** | We define our own structure. This is a feature here: we learn by making explicit choices. |

---

## Consequences

- The API lives in `apps/api/`
- All routes are `async def`
- All request/response types use Pydantic v2 schemas
- `uvicorn` with `--workers` or `gunicorn + uvicorn` workers for production
- Type checking with `mypy --strict` is enforced via pre-commit hooks

---

## Questions This Decision Answers in Interviews

**Q: Why FastAPI instead of Flask?**
Flask has no native async support and no automatic request validation.
FastAPI's Pydantic integration means invalid requests are rejected before touching business logic.

**Q: Why Python at all? Why not Go?**
The AI library ecosystem (embedding models, LLM clients, evaluation frameworks) is Python-first.
Forcing a Go or Rust backend would require bridging to Python anyway — at more complexity for no gain.

**Q: How does FastAPI handle concurrent LLM calls?**
Routes are `async def`. When one request is awaiting an LLM response, the event loop serves
other requests. One FastAPI process can handle many concurrent in-flight LLM calls.
