from __future__ import annotations

import json
from openai import OpenAI
from pathlib import Path
from .config import OPENAI_API_KEY, OPENAI_MODEL, LLM_DEBUG_DIR, LLM_DEBUG_ENABLED


client = OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """You are a SQL generator for SQLite.
Return ONLY valid JSON with keys: sql, explanation.
Rules:
- Only generate a single SELECT query.
- Do NOT use INSERT/UPDATE/DELETE/DROP/ALTER/CREATE/PRAGMA.
- Use only tables/columns from the provided schema.
- Prefer explicit JOINs.
- Keep results small (use LIMIT when appropriate).
"""


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def generate_sql_and_explanation(question: str, schema_text: str) -> dict:
    user_prompt = f"""DATABASE SCHEMA:
{schema_text}

USER QUESTION:
{question}

Return JSON only:
{{
  "sql": "...",
  "explanation": "..."
}}
"""
    
    request_payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
    }

    if LLM_DEBUG_ENABLED:
        try:
            _write_json(Path(LLM_DEBUG_DIR) / "llm_request.json", request_payload)

        except Exception as e:
            print(e)
    
    resp = client.chat.completions.create(
        model=request_payload["model"],
        messages=request_payload["messages"],
        temperature=request_payload["temperature"],
    )

    raw_content = (resp.choices[0].message.content or "").strip()

    # Robust JSON parsing (handle accidental markdown fences)
    cleaned = raw_content.replace("```json", "").replace("```", "").strip()

    data = json.loads(cleaned)

    if "sql" not in data or "explanation" not in data:
        raise ValueError("LLM output missing required keys: sql, explanation")

    if LLM_DEBUG_ENABLED:
        _write_json(Path(LLM_DEBUG_DIR) / "llm_response.json", data)
        _write_json(Path(LLM_DEBUG_DIR) / "llm_response_raw.json", {"content": raw_content})

    return data
