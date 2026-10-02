import re
import time
from typing import Any, Dict, List, Optional, Tuple
from google import genai
from google.genai import types
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.core.config import settings

# Database Schema Context for Gemini
DATABASE_SCHEMA_PROMPT = """
You are an expert PostgreSQL DBA and Data Analyst.
Translate the user's natural language question into a single valid, optimized PostgreSQL query based on the following database schema.

### TABLES & COLUMNS:

1. Table: `schemes` (Government Welfare Schemes)
   - `id`: INTEGER PRIMARY KEY
   - `name`: VARCHAR(255) (e.g. 'Pradhan Mantri Kisan Samman Nidhi')
   - `code`: VARCHAR(50) UNIQUE (e.g. 'PM-KISAN', 'PMAY-G', 'MGNREGA', 'AB-PMJAY', 'JJM', 'PM-POSHAN', 'PM-SVANIDHI', 'PLI-AUTO', 'SBM-U-2', 'SAMARTH')
   - `ministry`: VARCHAR(255) (e.g. 'Ministry of Agriculture and Farmers Welfare')
   - `sector`: VARCHAR(100) (e.g. 'Agriculture', 'Housing', 'Employment', 'Healthcare', 'Water & Sanitation', 'Education & Nutrition', 'Urban Livelihood', 'Manufacturing', 'Sanitation & Waste Management', 'Skill Development')
   - `description`: TEXT
   - `eligibility_criteria`: TEXT
   - `budget_allocated`: FLOAT (total national budget in Crores)
   - `is_active`: BOOLEAN
   - `launch_date`: DATE
   - `created_at`: TIMESTAMP WITH TIME ZONE
   - `updated_at`: TIMESTAMP WITH TIME ZONE

2. Table: `locations` (Geographic Regions)
   - `id`: INTEGER PRIMARY KEY
   - `state`: VARCHAR(100) (e.g. 'Maharashtra', 'Uttar Pradesh', 'Karnataka', 'Gujarat', 'Rajasthan', 'Madhya Pradesh', 'Bihar', 'Tamil Nadu', 'Odisha', 'Assam')
   - `district`: VARCHAR(100) (e.g. 'Pune', 'Varanasi', 'Bengaluru Rural', 'Ahmedabad', 'Jaipur', 'Indore', 'Patna', 'Coimbatore', 'Khordha', 'Kamrup')
   - `sub_district`: VARCHAR(100) (e.g. 'Haveli', 'Sadar', 'Hoskote', 'Daskroi', 'Sanganer', 'Sanwer', 'Danapur', 'Pollachi', 'Bhubaneswar', 'Guwahati')
   - `pincode`: VARCHAR(10)
   - `area_type`: VARCHAR(50) ('Rural', 'Urban', 'Semi-Urban')
   - `created_at`: TIMESTAMP WITH TIME ZONE
   - `updated_at`: TIMESTAMP WITH TIME ZONE

3. Table: `funds` (Scheme Fund Allocations and Utilization per Location)
   - `id`: INTEGER PRIMARY KEY
   - `scheme_id`: INTEGER (FOREIGN KEY -> schemes.id)
   - `location_id`: INTEGER (FOREIGN KEY -> locations.id)
   - `financial_year`: VARCHAR(20) (e.g. '2024-2025')
   - `allocated_amount`: FLOAT (in Crores)
   - `disbursed_amount`: FLOAT (in Crores)
   - `utilized_amount`: FLOAT (in Crores)
   - `status`: VARCHAR(50) (e.g. 'Partially Utilized', 'Disbursed', 'Fully Utilized', 'Under Execution', 'Under Review', 'Completed')
   - `sanction_date`: DATE
   - `created_at`: TIMESTAMP WITH TIME ZONE
   - `updated_at`: TIMESTAMP WITH TIME ZONE

### RULES FOR SQL GENERATION:
1. Return ONLY the raw SQL query. Do not wrap it in markdown code fences (no ```sql ... ```), do not include comments or explanations.
2. The query MUST be a read-only SELECT or WITH statement.
3. Use ILIKE or LOWER() for flexible, case-insensitive string matching.
4. Join tables logically when query spans multiple entities (e.g., JOIN schemes on funds.scheme_id = schemes.id JOIN locations on funds.location_id = locations.id).
5. Always order results meaningfully if ranking, highest/lowest amounts, or counts are requested.
6. Limit results to 50 rows maximum unless explicitly specified otherwise.
"""


def _get_gemini_client() -> genai.Client:
    api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GEMINI_API_KEY is not configured on the server.",
        )
    return genai.Client(api_key=api_key)


def sanitize_and_validate_sql(raw_sql: str) -> str:
    """
    Clean code fences/whitespace and validate that SQL is strictly read-only.
    """
    cleaned_sql = raw_sql.strip()

    # Remove markdown code blocks if Gemini enclosed them
    if cleaned_sql.startswith("```"):
        cleaned_sql = re.sub(r"^```(?:sql)?\s*", "", cleaned_sql, flags=re.IGNORECASE)
        cleaned_sql = re.sub(r"\s*```$", "", cleaned_sql)
        cleaned_sql = cleaned_sql.strip()

    # Remove trailing semicolon
    cleaned_sql = cleaned_sql.rstrip(";")

    # Security check: Disallow destructive/mutating statements
    forbidden_keywords = [
        r"\bINSERT\b",
        r"\bUPDATE\b",
        r"\bDELETE\b",
        r"\bDROP\b",
        r"\bALTER\b",
        r"\bTRUNCATE\b",
        r"\bCREATE\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
        r"\bEXEC\b",
        r"\bEXECUTE\b",
    ]

    for pattern in forbidden_keywords:
        if re.search(pattern, cleaned_sql, re.IGNORECASE):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Security violation: Mutating statement detected ({pattern}). Only read-only queries are permitted.",
            )

    # Must start with SELECT or WITH
    if not re.match(r"^\s*(SELECT|WITH)\b", cleaned_sql, re.IGNORECASE):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Generated query is not a valid SELECT statement.",
        )

    return cleaned_sql


async def generate_sql_from_question(question: str) -> str:
    """
    Uses Google Gemini API to translate a natural language question into PostgreSQL.
    """
    client = _get_gemini_client()

    prompt = f"""
{DATABASE_SCHEMA_PROMPT}

User Question: {question}
SQL Query:
"""
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
            ),
        )
        if not response.text:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API returned an empty response.",
            )

        sql_query = sanitize_and_validate_sql(response.text)
        return sql_query
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gemini API error during SQL generation: {str(e)}",
        )


async def execute_sql_query(sql_query: str, db: AsyncSession) -> List[Dict[str, Any]]:
    """
    Executes the validated SQL query on Supabase PostgreSQL and returns list of dictionaries.
    """
    try:
        result = await db.execute(text(sql_query))
        rows = result.mappings().all()
        # Convert row mappings to standard JSON-serializable dictionaries
        serialized_rows: List[Dict[str, Any]] = []
        for row in rows:
            row_dict = {}
            for k, v in row.items():
                if hasattr(v, "isoformat"):
                    row_dict[k] = v.isoformat()
                else:
                    row_dict[k] = v
            serialized_rows.append(row_dict)
        return serialized_rows
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error executing generated SQL on Supabase database: {str(e)} | SQL: {sql_query}",
        )


async def generate_result_summary(question: str, sql_query: str, results: List[Dict[str, Any]]) -> str:
    """
    Generates a concise natural language explanation/summary of the database results.
    """
    client = _get_gemini_client()

    # Limit sample rows sent to summary to prevent token overflow
    sample_results = results[:20]

    prompt = f"""
You are an AI analyst. A user asked a question about government schemes and funding data.
The database query has been executed and returned the results below.

Question: {question}
SQL Query: {sql_query}
Query Results ({len(results)} rows total):
{sample_results}

Provide a concise, direct, and professional 1-3 sentence summary answering the user's question based on these results.
"""
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        return response.text.strip() if response.text else "Query executed successfully."
    except Exception:
        return "Query executed successfully."


async def process_natural_language_query(
    question: str,
    include_summary: bool,
    db: AsyncSession,
) -> Tuple[str, List[Dict[str, Any]], Optional[str], float]:
    """
    Orchestrates NL -> SQL -> Execution -> Summary.
    """
    start_time = time.time()

    # 1. Translate question to SQL via Gemini
    sql_query = await generate_sql_from_question(question)

    # 2. Execute SQL query on Supabase
    results = await execute_sql_query(sql_query, db)

    # 3. Generate summary if requested
    summary = None
    if include_summary:
        summary = await generate_result_summary(question, sql_query, results)

    execution_time_ms = round((time.time() - start_time) * 1000, 2)
    return sql_query, results, summary, execution_time_ms
