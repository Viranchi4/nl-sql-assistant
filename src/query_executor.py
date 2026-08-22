# src/query_executor.py
"""
query_executor
Safe MySQL executor using mysql-connector-python connection pooling.
Reads connection info from environment variables for portability.
Returns query results as list of dicts.
"""

import os
from typing import List, Dict, Tuple, Any, Optional
import mysql.connector
from mysql.connector import pooling

# Read connection settings from environment with sensible defaults
DB_CONFIG = {
    "host": os.getenv("SA_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("SA_DB_PORT", "3306")),
    "user": os.getenv("SA_DB_USER", "root"),
    "password": os.getenv("SA_DB_PASSWORD", ""),
    "database": os.getenv("SA_DB_NAME", "sales_analytics_db"),
    "charset": "utf8mb4",
    "use_unicode": True,
}

# Pool settings
POOL_NAME = "sa_pool"
POOL_SIZE = int(os.getenv("SA_DB_POOL_SIZE", "3"))

_pool: Optional[pooling.MySQLConnectionPool] = None

def init_pool() -> None:
    """Initialize the connection pool (idempotent)."""
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name=POOL_NAME,
            pool_size=POOL_SIZE,
            **DB_CONFIG
        )

def _get_conn():
    """Get a connection from the pool, initializing if necessary."""
    if _pool is None:
        init_pool()
    return _pool.get_connection()

def execute_query(sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    """
    Execute a read-only SELECT query and return rows as list of dicts.
    Always use parameterized queries to avoid injection.
    """
    conn = _get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        if cursor.description:
            cols = [d[0] for d in cursor.description]
            result = [dict(zip(cols, r)) for r in rows]
        else:
            result = []
        cursor.close()
        return result
    finally:
        conn.close()

def execute_write(sql: str, params: Tuple = ()) -> int:
    """
    Execute an INSERT/UPDATE/DELETE and return affected row count.
    Commits on success.
    """
    conn = _get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected
    finally:
        conn.close()

if __name__ == "__main__":
    # Quick smoke test (requires env vars or defaults)
    try:
        init_pool()
        print("Connection pool initialized")
        rows = execute_query("SELECT COUNT(*) AS cnt FROM customers;")
        print("customers count:", rows)
    except Exception as e:
        print("DB test failed:", e)
