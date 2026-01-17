from __future__ import annotations

import sqlite3
from typing import Any, List, Tuple

from .config import DB_PATH


def run_select(sql: str) -> Tuple[List[str], List[List[Any]]]:
    """
    Executes a SELECT query and returns (columns, rows).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        data = [[row[c] for c in cols] for row in rows]
        return cols, data
    finally:
        conn.close()
