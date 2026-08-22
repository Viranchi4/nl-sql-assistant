# src/app.py
"""
Simple CLI for the NL -> SQL assistant.
Run: python -m src.app
Type a natural language query and press Enter.
Type 'exit' or Ctrl+C to quit.
"""

import os
import sys
import re
from src.env_loader import load_env
load_env()

from typing import List, Dict, Any
from src import nl_to_sql
from src import query_executor
from tabulate import tabulate

def print_table(rows: List[Dict[str, Any]]) -> None:
    if not rows:
        print("(no rows)")
        return
    cols = list(rows[0].keys())
    table = [[r.get(c, "") for c in cols] for r in rows]
    print(tabulate(table, headers=cols, tablefmt="github"))

DESTRUCTIVE_SQL_PATTERN = re.compile(
    r'\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|REPLACE)\b',
    flags=re.IGNORECASE
)

def is_safe_sql(sql: str) -> bool:
    """Return False if SQL contains destructive statements."""
    if not sql:
        return True
    return DESTRUCTIVE_SQL_PATTERN.search(sql) is None

def main() -> None:
    # initialize DB pool
    try:
        query_executor.init_pool()
    except Exception as e:
        print("Failed to initialize DB connection pool:", e)
        sys.exit(1)

    print("NL→SQL assistant (type 'exit' to quit)")
    try:
        while True:
            nl = input("\nEnter query: ").strip()
            if not nl:
                continue
            if nl.lower() in ("exit", "quit"):
                break

            sql, params = nl_to_sql.map_to_sql(nl)
            if sql is None:
                print("Sorry — I couldn't map that request to a SQL template.")
                continue

            if not is_safe_sql(sql):
                print("Refusing to execute potentially destructive SQL. Only read-only queries are allowed.")
                print(f"Generated SQL (not executed): {sql}")
                continue

            try:
                rows = query_executor.execute_query(sql, params or ())
                print_table(rows)
            except Exception as e:
                print("Query execution failed:", e)
    except KeyboardInterrupt:
        print("\nGoodbye")

if __name__ == "__main__":
    main()
