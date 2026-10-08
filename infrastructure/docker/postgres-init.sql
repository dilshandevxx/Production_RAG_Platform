-- ─────────────────────────────────────────────────────────────────────────────
-- postgres-init.sql
-- Runs ONCE when the PostgreSQL container is first created.
--
-- WHY: We need to enable the pgvector extension. This can't be done in
-- application code (it requires superuser privileges). The init script runs
-- as the postgres superuser before our app ever connects.
-- ─────────────────────────────────────────────────────────────────────────────

-- Enable the pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable uuid-ossp for UUID generation in PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pg_trgm for fuzzy text search (used in keyword retrieval)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Confirm extensions are installed
SELECT extname, extversion FROM pg_extension
WHERE extname IN ('vector', 'uuid-ossp', 'pg_trgm');
