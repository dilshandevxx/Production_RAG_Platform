"""
Phase 0 smoke test.

WHY this test exists:
    Every phase should have at least one test that confirms the basics work.
    This test doesn't test any RAG logic — it verifies the testing
    infrastructure itself is wired up correctly.

Run with: pytest tests/unit/test_phase0_smoke.py -v
"""

import sys
from pathlib import Path


def test_python_version() -> None:
    """Confirm we're running on Python 3.12+."""
    assert sys.version_info >= (3, 12), (
        f"Project requires Python 3.12+, running {sys.version_info}"
    )


def test_project_structure_exists() -> None:
    """Confirm the expected directories exist."""
    root = Path(__file__).parent.parent.parent  # project root

    required_dirs = [
        "apps/api",
        "services/ingestion",
        "services/worker",
        "packages/rag",
        "packages/database",
        "packages/embeddings",
        "packages/llm",
        "packages/observability",
        "tests/unit",
        "tests/integration",
        "tests/security",
        "tests/rag",
        "docs/adr",
        "evaluations/datasets",
        "infrastructure/docker",
    ]

    for directory in required_dirs:
        path = root / directory
        assert path.exists(), f"Missing required directory: {directory}"
        assert path.is_dir(), f"Expected directory but found file: {directory}"


def test_adr_001_exists() -> None:
    """Confirm ADR-001 has been written — architecture thinking before code."""
    root = Path(__file__).parent.parent.parent
    adr_path = root / "docs/adr/ADR-001-python-fastapi.md"
    assert adr_path.exists(), "ADR-001 must be written before Phase 1 starts"
    content = adr_path.read_text(encoding="utf-8")
    # ADR must contain all required sections
    assert "## Context" in content, "ADR must have a Context section"
    assert "## Decision" in content, "ADR must have a Decision section"
    assert "## Trade-offs" in content, "ADR must have a Trade-offs section"


def test_env_example_exists_but_not_env() -> None:
    """
    .env.example MUST exist (it's the config contract).
    .env must NOT be in the repo (it contains secrets).

    This test verifies the security discipline is in place.
    """
    root = Path(__file__).parent.parent.parent
    assert (root / ".env.example").exists(), ".env.example must be committed"
    # .env should be gitignored — it may exist locally but must never be committed.
    # We can't test git status here, but we can verify .gitignore covers it.
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore, ".env must be in .gitignore"


def test_core_imports() -> None:
    """Confirm critical dependencies are installed and importable."""
    import fastapi  # noqa: F401
    import pydantic  # noqa: F401
    import sqlalchemy  # noqa: F401
    import alembic  # noqa: F401
    import redis  # noqa: F401
    import openai  # noqa: F401
    import structlog  # noqa: F401
    import numpy  # noqa: F401
    import tenacity  # noqa: F401
