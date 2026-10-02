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
    sql_query, results, summary, execution_time = await process_natural_language_query(
        question=query_in.question,
        include_summary=query_in.include_summary,
        db=db,
    )

    return NaturalLanguageQueryResponse(
        question=query_in.question,
        sql_query=sql_query,
        results=results,
        row_count=len(results),
        summary=summary,
        execution_time_ms=execution_time,
    )
