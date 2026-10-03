# BharatGeo Insights Backend API

A production-ready, asynchronous **FastAPI** backend integrated with **Supabase PostgreSQL** via **SQLAlchemy 2.0** and **asyncpg**.

---

## =ƒÜÇ Features

- **FastAPI**: High performance, type-safe API framework with automatic OpenAPI / Swagger documentation.
- **Supabase PostgreSQL Integration**: Fully asynchronous connection pooling via SQLAlchemy 2.0 & `asyncpg` with URL-safe credential handling.
- **Supabase Python Client**: Built-in wrapper for Auth, Storage, and Realtime event subscriptions.
- **Modular Architecture**: Layered architecture separated into `core`, `models`, `schemas`, and `api/v1` routers.
- **Health Check Endpoint**: Real-time database ping to verify PostgreSQL connectivity and version.
- **CRUD Operations**: Sample async CRUD endpoint (`/api/v1/items/`) using SQLAlchemy 2.0 mapped models.
- **Automated Testing**: Preconfigured `pytest` + `pytest-asyncio` test suite.

---

## =ƒôü Project Structure

```text
BharatGeo Insights/
Gö£GöÇGöÇ app/
Göé   Gö£GöÇGöÇ __init__.py
Göé   Gö£GöÇGöÇ main.py                  # FastAPI application entrypoint & lifespan
Göé   Gö£GöÇGöÇ api/
Göé   Göé   Gö£GöÇGöÇ __init__.py
Göé   Göé   GööGöÇGöÇ v1/
Göé   Göé       Gö£GöÇGöÇ router.py        # Aggregated v1 router
Göé   Göé       GööGöÇGöÇ endpoints/
Göé   Göé           Gö£GöÇGöÇ health.py    # Database & service health check
Göé   Göé           GööGöÇGöÇ items.py     # Sample async CRUD endpoints
Göé   Gö£GöÇGöÇ core/
Göé   Göé   Gö£GöÇGöÇ __init__.py
Göé   Göé   Gö£GöÇGöÇ config.py            # Pydantic Settings & environment loader
Göé   Göé   Gö£GöÇGöÇ database.py          # SQLAlchemy async engine, sessionmaker & get_db dependency
Göé   Göé   GööGöÇGöÇ supabase.py          # Official Supabase Python SDK client wrapper
Göé   Gö£GöÇGöÇ models/
Göé   Göé   Gö£GöÇGöÇ __init__.py
Göé   Göé   Gö£GöÇGöÇ base.py              # DeclarativeBase
Göé   Göé   GööGöÇGöÇ item.py              # Sample SQLAlchemy ORM model
Göé   GööGöÇGöÇ schemas/
Göé       Gö£GöÇGöÇ __init__.py
Göé       Gö£GöÇGöÇ health.py            # Pydantic models for health check
Göé       GööGöÇGöÇ item.py              # Pydantic models for Item CRUD
Gö£GöÇGöÇ tests/
Göé   Gö£GöÇGöÇ conftest.py              # Pytest async fixtures
Göé   GööGöÇGöÇ test_api.py              # Automated test suite
Gö£GöÇGöÇ .env                         # Environment variables (secret)
Gö£GöÇGöÇ .env.example                 # Environment variables template
Gö£GöÇGöÇ .gitignore
Gö£GöÇGöÇ create_tables.py             # Utility to initialize database tables in Supabase
Gö£GöÇGöÇ pytest.ini                   # Pytest async configuration
Gö£GöÇGöÇ requirements.txt             # Project dependencies
GööGöÇGöÇ README.md
```

---

## =ƒ¢án+Å Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Virtual Environment

### 2. Setup Virtual Environment & Install Dependencies

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows PowerShell:
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Your `.env` file is preconfigured with your Supabase PostgreSQL credentials:

```ini
PROJECT_NAME="BharatGeo Insights API"
PROJECT_VERSION="1.0.0"
API_V1_STR="/api/v1"
ENVIRONMENT="development"
DEBUG=True

# Supabase Database URL (password special characters URL-encoded)
DATABASE_URL=postgresql+asyncpg://postgres:Ath%40rva1509@db.dpllfhgragqlkecedfds.supabase.co:5432/postgres

# Supabase API credentials (optional for Auth & Storage)
SUPABASE_URL=https://dpllfhgragqlkecedfds.supabase.co
SUPABASE_KEY=your-supabase-anon-key
```

### 4. Create Database Tables & Seed Dummy Data

Run the seeding script to create tables and insert 10 rows of dummy data into `schemes`, `locations`, and `funds`:
```powershell
python seed_data.py
```

### 5. Run the Server

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Interactive API Docs (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check Endpoint**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
- **AI Natural Language to SQL Query**: `POST /api/v1/query/ask`
- **Government Schemes**: [http://localhost:8000/api/v1/schemes/](http://localhost:8000/api/v1/schemes/)
- **Locations**: [http://localhost:8000/api/v1/locations/](http://localhost:8000/api/v1/locations/)
- **Fund Allocations**: [http://localhost:8000/api/v1/funds/](http://localhost:8000/api/v1/funds/)

---

## =ƒñû AI Natural Language Query (`/api/v1/query/ask`)

Ask any question in plain English. The endpoint translates it to PostgreSQL using Gemini AI, executes it on Supabase, and returns the data with an AI summary.

### Example Request:
```bash
curl -X POST "http://localhost:8000/api/v1/query/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "Which schemes have allocated funds in Maharashtra?", "include_summary": true}'
```

### Example Response:
```json
{
  "question": "Which schemes have allocated funds in Maharashtra?",
  "sql_query": "SELECT DISTINCT s.name FROM schemes AS s JOIN funds AS f ON s.id = f.scheme_id JOIN locations AS l ON f.location_id = l.id WHERE l.state ILIKE 'Maharashtra'",
  "results": [
    {
      "name": "Pradhan Mantri Kisan Samman Nidhi"
    }
  ],
  "row_count": 1,
  "summary": "Pradhan Mantri Kisan Samman Nidhi is the scheme that has allocated funds in Maharashtra.",
  "execution_time_ms": 1420.5
}
```

---

## =ƒº¬ Running Tests

```powershell
pytest -v
```

## How to present this project (Trick Questions)
Ask any of the following queries in the UI to demonstrate the intelligence Engine:
* Show me the state-wise distribution of delayed MGNREGA wage payments across India for the last financial year. (Demonstrates Map capabilities)
* Compare the total PM-Kisan funds disbursed versus the number of registered beneficiaries for the top 5 districts in Maharashtra, and calculate the percentage of funds successfully credited. (Demonstrates Tabular data)
* What is the primary reason for the highest number of failed Jal Shakti water project implementations in rural areas? (Demonstrates Text Insights)
* How has the seasonal employment generated by MGNREGA fluctuated month-over-month compared to the previous year? Show me the trend. (Demonstrates Charting)

## Recent Updates (v1.0.1)
- **UI & UX Enhancements**: Implemented a modern dark-mode aesthetic with custom glowing cursor effects, interactive radial background glow, and smooth hover transitions to provide a premium user experience.
- **AI Model Upgrade**: Migrated the core intelligence engine from gemini-2.5-flash to the highly capable gemini-1.5-pro model to handle more complex Natural Language to SQL generation with higher accuracy.
- **Resiliency & Fallbacks**: Engineered robust fallback mechanisms to handle Google API rate limits and 503 Service Unavailable errors, ensuring the platform remains 100% functional during high-traffic hackathon demos.
- **Rebranding**: Successfully rebranded the entire ecosystem from Elevate to BharatGeo Insights to better align with the core problem statement.
