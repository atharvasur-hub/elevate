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
async def test_locations_api(client):
    response = await client.get("/api/v1/locations/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 35
    states = [loc["state"] for loc in data]
    assert "Maharashtra" in states
    assert "Gujarat" in states
    # Verify geo-coordinates exist on locations
    assert all("latitude" in loc and "longitude" in loc for loc in data)
    assert all(loc["latitude"] is not None and loc["longitude"] is not None for loc in data)


@pytest.mark.asyncio
async def test_natural_language_query_api_maharashtra(client):
    response = await client.post(
        "/api/v1/query/ask",
        json={"question": "Which agriculture scheme records have allocated funds in Maharashtra?", "include_summary": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert "SELECT" in data["sql_query"].upper()
    assert data["display_type"] in ["map", "bar_chart", "table", "text"]
    assert data["ai_summary"] is not None
    assert "traceability_rows" in data
    assert isinstance(data["traceability_rows"], list)
    assert len(data["traceability_rows"]) > 0
    # Verify geo-coordinates are included in traceability rows
    first_row = data["traceability_rows"][0]
    assert "latitude" in first_row or "district" in first_row


@pytest.mark.asyncio
async def test_natural_language_query_api_water(client):
    response = await client.post(
        "/api/v1/query/ask",
        json={"question": "Show all water scheme tap connections with cost incurred.", "include_summary": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert "water_scheme" in data["sql_query"].lower()
    assert len(data["traceability_rows"]) > 0


@pytest.mark.asyncio
async def test_natural_language_query_api_rural(client):
    response = await client.post(
        "/api/v1/query/ask",
        json={"question": "What is the average wages paid per project type in rural dev scheme?", "include_summary": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert "rural_dev_scheme" in data["sql_query"].lower()
    assert len(data["traceability_rows"]) > 0
