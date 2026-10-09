import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# Load DB URL from env, default to local postgres if not set
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://rag_user:rag_password@localhost:5432/rag_db"
)

# Engine configured for asyncpg
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=int(os.getenv("DATABASE_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DATABASE_MAX_OVERFLOW", "20")),
)

# Session factory
async_session_maker = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Declarative base for SQLAlchemy models
Base = declarative_base()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to be used in FastAPI routes for getting a database session.
    """
    async with async_session_maker() as session:
        yield session
