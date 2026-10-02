from collections.abc import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

from app.core.config import settings

# In testing or serverless setups, NullPool prevents cross-event-loop connection issues on Windows
# In production, AsyncAdaptedQueuePool manages connection pools efficiently.
pool_class = NullPool if settings.ENVIRONMENT in ["test", "testing"] else AsyncAdaptedQueuePool

engine_kwargs = {
    "echo": settings.DEBUG,
    "future": True,
}

if pool_class is AsyncAdaptedQueuePool:
    engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    })
else:
    engine_kwargs.update({
        "poolclass": NullPool,
    })

# Create Async Engine for Supabase PostgreSQL
engine: AsyncEngine = create_async_engine(
    settings.async_database_url,
    **engine_kwargs
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base model class for all SQLAlchemy models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async database session
    and guarantees proper closing upon request lifecycle completion.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection() -> dict[str, str]:
    """
    Utility to verify live connectivity to Supabase PostgreSQL database.
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT version();"))
            db_version = result.scalar()
            return {
                "status": "healthy",
                "database": "Supabase PostgreSQL",
                "version": str(db_version),
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "Supabase PostgreSQL",
            "error": str(e),
        }
