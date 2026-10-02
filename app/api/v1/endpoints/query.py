from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.query import NaturalLanguageQueryRequest, NaturalLanguageQueryResponse
from app.services.nl_query_service import process_natural_language_query

router = APIRouter()


@router.post(
    "/ask",
    response_model=NaturalLanguageQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Natural Language to SQL Query & Execution",
    description="Translates a natural language question into PostgreSQL using Gemini AI, executes it on the Supabase database, and returns the query results along with an AI summary.",
)
async def ask_database(
    query_in: NaturalLanguageQueryRequest,
    db: AsyncSession = Depends(get_db),
):
    plan_result = await process_natural_language_query(
        question=query_in.question,
        include_summary=query_in.include_summary,
        db=db,
    )

    traceability_rows = plan_result["traceability_rows"]
    ai_summary = plan_result["ai_summary"] if query_in.include_summary else None

    return NaturalLanguageQueryResponse(
        question=query_in.question,
        sql_query=plan_result["sql_query"],
        display_type=plan_result["display_type"],
        ai_summary=ai_summary,
        traceability_rows=traceability_rows,
        results=traceability_rows,
        row_count=len(traceability_rows),
        summary=ai_summary,
        execution_time_ms=plan_result["execution_time_ms"],
    )

