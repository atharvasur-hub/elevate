import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"]["status"] == "healthy"
    assert "Supabase PostgreSQL" in data["database"]["database"]


@pytest.mark.asyncio
async def test_schemes_api(client):
    response = await client.get("/api/v1/schemes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    codes = [s["code"] for s in data]
    assert "PM-KISAN" in codes
    assert "MGNREGA" in codes


@pytest.mark.asyncio
async def test_locations_api(client):
    response = await client.get("/api/v1/locations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    states = [loc["state"] for loc in data]
    assert "Maharashtra" in states
    assert "Karnataka" in states


@pytest.mark.asyncio
async def test_funds_api(client):
    response = await client.get("/api/v1/funds/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    assert data[0]["scheme"] is not None
    assert data[0]["location"] is not None


@pytest.mark.asyncio
async def test_natural_language_query_api(client):
    response = await client.post(
        "/api/v1/query/ask",
        json={"question": "What are the names of all schemes?", "include_summary": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert "SELECT" in data["sql_query"].upper()
    assert data["row_count"] >= 10
    assert len(data["results"]) >= 10
    assert data["summary"] is not None
