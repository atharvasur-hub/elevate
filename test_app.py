import asyncio
import json
from app.main import app
from httpx import ASGITransport, AsyncClient


async def test_nl_queries():
    questions = [
        "Which schemes have allocated funds in Maharashtra?",
        "What are the top 3 schemes with the highest total national budget allocated?",
        "List all locations where fund status is 'Fully Utilized'.",
        "Show total disbursed amount across all funds.",
    ]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        for q in questions:
            print("=" * 70)
            print(f"QUESTION: {q}")
            resp = await ac.post("/api/v1/query/ask", json={"question": q, "include_summary": True})
            print(f"STATUS: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                print(f"SQL GENERATED:\n{data['sql_query']}")
                print(f"ROWS RETURNED: {data['row_count']}")
                print(f"RESULTS: {json.dumps(data['results'], indent=2)}")
                print(f"AI SUMMARY:\n{data['summary']}")
                print(f"LATENCY: {data['execution_time_ms']} ms")
            else:
                print("ERROR:", resp.text)
            print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_nl_queries())
