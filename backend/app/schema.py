from __future__ import annotations

import sqlite3
from .config import DB_PATH


def get_schema_text() -> str:
    """
    Returns a compact schema description for prompting.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()

        lines: list[str] = []
        for (tname,) in tables:
            cols = conn.execute(f"PRAGMA table_info({tname})").fetchall()
            col_names = [c[1] for c in cols]  # PRAGMA table_info: (cid, name, type, notnull, dflt_value, pk)
            lines.append(f"Table {tname}({', '.join(col_names)})")
        return "\n".join(lines)
    finally:
        conn.close()


def get_allowed_tables() -> set[str]:
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        return {r[0].lower() for r in rows}
    finally:
        conn.close()
