from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, List, Optional


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class QueryResponse(BaseModel):
    sql: str
    columns: List[str]
    rows: List[List[Any]]
    explanation: str
    warnings: Optional[List[str]] = None
