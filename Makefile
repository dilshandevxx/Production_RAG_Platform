# ─────────────────────────────────────────────────────────────────────────────
# Makefile — Project command center
#
# WHY: Standardized commands so any developer (or CI) runs the same thing.
# `make dev` is all you need to start. `make test` runs the full test suite.
# ─────────────────────────────────────────────────────────────────────────────

.PHONY: help install dev infra-up infra-down infra-fresh lint format typecheck test test-unit test-integration test-security migrate migrate-create clean

# ─── Default target: show help ────────────────────────────────────────────────
help:
	@echo ""
	@echo "Production RAG Platform — Available Commands"
	@echo "═══════════════════════════════════════════"
	@echo "  make install         Install Python dependencies (dev + test)"
	@echo "  make hooks           Install pre-commit hooks"
	@echo ""
	@echo "  make infra-up        Start local infrastructure (DB, Redis, MinIO, observability)"
	@echo "  make infra-down      Stop infrastructure (data preserved)"
	@echo "  make infra-fresh     Stop + delete all data volumes (clean slate)"
	@echo ""
	@echo "  make lint            Run ruff linter"
	@echo "  make format          Run ruff formatter"
	@echo "  make typecheck       Run mypy type checker"
	@echo "  make check           Run lint + format + typecheck (full quality check)"
	@echo ""
	@echo "  make test            Run all tests"
	@echo "  make test-unit       Run unit tests only (fast, no infra needed)"
	@echo "  make test-int        Run integration tests (requires infra)"
	@echo "  make test-security   Run tenant isolation and security tests"
	@echo "  make test-rag        Run RAG quality tests"
	@echo ""
	@echo "  make migrate         Apply database migrations"
	@echo "  make migrate-create  Create a new migration (NAME=migration_name)"
	@echo ""
	@echo "  make clean           Remove Python cache files"
	@echo ""

# ─── Setup ───────────────────────────────────────────────────────────────────
install:
	pip install -e ".[dev,test]"

hooks:
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "✅ Pre-commit hooks installed. They run on every git commit."

# ─── Infrastructure ───────────────────────────────────────────────────────────
infra-up:
	@echo "Starting local infrastructure..."
	docker compose up -d
	@echo ""
	@echo "✅ Infrastructure running:"
	@echo "   PostgreSQL : localhost:5432  (rag_user / rag_password)"
	@echo "   Redis      : localhost:6379"
	@echo "   MinIO UI   : http://localhost:9001  (minioadmin / minioadmin)"
	@echo "   Prometheus : http://localhost:9090"
	@echo "   Grafana    : http://localhost:3001  (admin / admin)"
	@echo "   Jaeger UI  : http://localhost:16686"

infra-down:
	docker compose down

infra-fresh:
	@echo "⚠️  This will DELETE all local data volumes."
	docker compose down -v
	@echo "✅ All volumes deleted. Run 'make infra-up' for a clean start."

infra-logs:
	docker compose logs -f $(service)

# ─── Code quality ─────────────────────────────────────────────────────────────
lint:
	ruff check apps/ services/ packages/ tests/

format:
	ruff format apps/ services/ packages/ tests/

typecheck:
	mypy apps/ services/ packages/

check: format lint typecheck
	@echo "✅ All quality checks passed."

# ─── Testing ──────────────────────────────────────────────────────────────────
test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v -m unit

test-int:
	pytest tests/integration/ -v -m integration

test-security:
	pytest tests/security/ -v -m security

test-rag:
	pytest tests/rag/ -v -m rag

test-coverage:
	pytest tests/ --cov=apps --cov=services --cov=packages --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

# ─── Database migrations ──────────────────────────────────────────────────────
migrate:
	alembic upgrade head

migrate-create:
	@if [ -z "$(NAME)" ]; then echo "Usage: make migrate-create NAME=your_migration_name"; exit 1; fi
	alembic revision --autogenerate -m "$(NAME)"

migrate-down:
	alembic downgrade -1

migrate-history:
	alembic history --verbose

# ─── Cleanup ──────────────────────────────────────────────────────────────────
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache files cleaned."
