from __future__ import annotations

import re
import sqlparse


DISALLOWED = {"insert", "update", "delete", "drop", "alter", "create", "attach", "detach", "pragma", "truncate"}


def _first_keyword(sql: str) -> str:
    parsed = sqlparse.parse(sql)
    if not parsed:
        return ""
    stmt = parsed[0]
    for tok in stmt.tokens:
        if tok.is_whitespace:
            continue
        value = tok.value.strip().lower()
        # handle comments etc.
        value = re.sub(r"^--.*?$", "", value).strip()
        if value:
            return value.split()[0]
    return ""


def ensure_select_only(sql: str) -> None:
    kw = _first_keyword(sql)
    if kw != "select":
        raise ValueError("Only SELECT queries are allowed.")


def ensure_no_disallowed_keywords(sql: str) -> None:
    s = sql.lower()
    for bad in DISALLOWED:
        if re.search(rf"\b{re.escape(bad)}\b", s):
            raise ValueError(f"Disallowed keyword detected: {bad}")


def ensure_limit(sql: str, default_limit: int = 100) -> str:
    # If LIMIT exists, keep it. Otherwise add LIMIT.
    s = sql.strip().rstrip(";")
    if re.search(r"\blimit\b", s, flags=re.IGNORECASE):
        return s + ";"
    return f"{s}\nLIMIT {default_limit};"


def ensure_only_allowed_tables(sql: str, allowed_tables: set[str]) -> None:
    """
    Simple table name check:
    - Extract tokens after FROM/JOIN and verify they exist.
    - Not a full SQL parser, but good enough for project + report.
    """
    tokens = sqlparse.parse(sql)
    if not tokens:
        raise ValueError("Invalid SQL.")
    stmt = tokens[0]
    s = stmt.value

    # crude extraction: words after FROM or JOIN
    candidates = re.findall(r"\b(from|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)", s, flags=re.IGNORECASE)
    used = {name.lower() for _, name in candidates}

    unknown = sorted([t for t in used if t not in allowed_tables])
    if unknown:
        raise ValueError(f"Query uses unknown or disallowed tables: {', '.join(unknown)}")


def validate_and_normalize_sql(sql: str, allowed_tables: set[str]) -> str:
    sql = sql.strip()
    ensure_select_only(sql)
    ensure_no_disallowed_keywords(sql)
    ensure_only_allowed_tables(sql, allowed_tables)
    sql = ensure_limit(sql, default_limit=100)
    return sql
