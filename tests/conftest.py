import os

# Set environment before loading app
os.environ["ENVIRONMENT"] = "testing"

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.database import engine


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    await engine.dispose()
