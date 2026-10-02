from typing import Any, Dict, List, Optional
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
    results: List[Dict[str, Any]]
    row_count: int
    summary: Optional[str] = None
    execution_time_ms: float
