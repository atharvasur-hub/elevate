import asyncio
from app.core.database import Base, engine
import app.models  # noqa: F401


async def init_models():
    """Create database tables defined in SQLAlchemy models."""
    async with engine.begin() as conn:
        print("Creating tables in Supabase PostgreSQL...")
        await conn.run_sync(Base.metadata.create_all)
        print("[SUCCESS] Tables created successfully in Supabase!")


if __name__ == "__main__":
    asyncio.run(init_models())
