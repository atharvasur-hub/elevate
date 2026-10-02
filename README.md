# Elevate Backend API

A production-ready, asynchronous **FastAPI** backend integrated with **Supabase PostgreSQL** via **SQLAlchemy 2.0** and **asyncpg**.

---

## 🚀 Features

- **FastAPI**: High performance, type-safe API framework with automatic OpenAPI / Swagger documentation.
- **Supabase PostgreSQL Integration**: Fully asynchronous connection pooling via SQLAlchemy 2.0 & `asyncpg` with URL-safe credential handling.
- **Supabase Python Client**: Built-in wrapper for Auth, Storage, and Realtime event subscriptions.
- **Modular Architecture**: Layered architecture separated into `core`, `models`, `schemas`, and `api/v1` routers.
- **Health Check Endpoint**: Real-time database ping to verify PostgreSQL connectivity and version.
- **CRUD Operations**: Sample async CRUD endpoint (`/api/v1/items/`) using SQLAlchemy 2.0 mapped models.
- **Automated Testing**: Preconfigured `pytest` + `pytest-asyncio` test suite.

---

## 📁 Project Structure

```text
elevate/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entrypoint & lifespan
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── router.py        # Aggregated v1 router
│   │       └── endpoints/
│   │           ├── health.py    # Database & service health check
│   │           └── items.py     # Sample async CRUD endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Pydantic Settings & environment loader
│   │   ├── database.py          # SQLAlchemy async engine, sessionmaker & get_db dependency
│   │   └── supabase.py          # Official Supabase Python SDK client wrapper
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py              # DeclarativeBase
│   │   └── item.py              # Sample SQLAlchemy ORM model
│   └── schemas/
│       ├── __init__.py
│       ├── health.py            # Pydantic models for health check
│       └── item.py              # Pydantic models for Item CRUD
├── tests/
│   ├── conftest.py              # Pytest async fixtures
│   └── test_api.py              # Automated test suite
├── .env                         # Environment variables (secret)
├── .env.example                 # Environment variables template
├── .gitignore
├── create_tables.py             # Utility to initialize database tables in Supabase
├── pytest.ini                   # Pytest async configuration
├── requirements.txt             # Project dependencies
└── README.md
```

---

## 🛠️ Getting Started

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
PROJECT_NAME="Elevate API"
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

## 🤖 AI Natural Language Query (`/api/v1/query/ask`)

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

## 🧪 Running Tests

```powershell
pytest -v
```