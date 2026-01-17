from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import QueryRequest, QueryResponse
from .db import run_select
from .schema import get_schema_text, get_allowed_tables
from .validator import validate_and_normalize_sql
from .llm import generate_sql_and_explanation

app = FastAPI(title="Natural Language DB Interface", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty.")

    # 1) schema
    schema_text = get_schema_text()
    allowed_tables = get_allowed_tables()

    # 2) LLM generates SQL + explanation
    try:
        llm_out = generate_sql_and_explanation(question, schema_text)
        raw_sql = llm_out["sql"]
        explanation = llm_out["explanation"]
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM generation failed: {e}")

    # 3) validate + normalize
    try:
        sql = validate_and_normalize_sql(raw_sql, allowed_tables=allowed_tables)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL rejected by validator: {e}")

    # 4) execute
    try:
        columns, rows = run_select(sql)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL execution failed: {e}")

    return QueryResponse(
        sql=sql,
        columns=columns,
        rows=rows,
        explanation=explanation,
        warnings=None,
    )
