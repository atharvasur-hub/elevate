from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class NaturalLanguageQueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        description="The natural language question to translate into SQL (e.g., 'What are the top 3 schemes with the highest budget allocated?')",
        examples=["Which schemes have allocated funds in Maharashtra?"],
    )
    include_summary: bool = Field(
        True,
        description="Whether to generate an AI natural language summary of the query results.",
    )


class NaturalLanguageQueryResponse(BaseModel):
    question: str
    sql_query: str
    display_type: Literal["map", "bar_chart", "table", "text"] = Field(
        ...,
        description="Recommended display visualization: 'map', 'bar_chart', 'table', or 'text'",
    )
    ai_summary: Optional[str] = Field(
        None,
        description="Natural language summary / insights from AI",
    )
    traceability_rows: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Raw resulting rows executed against Supabase PostgreSQL",
    )
    results: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Raw resulting rows for backward compatibility",
    )
    row_count: int
    summary: Optional[str] = None
    execution_time_ms: float
