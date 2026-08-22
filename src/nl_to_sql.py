# src/nl_to_sql.py
"""
nl_to_sql
Simple rule-based NL -> SQL mapper for the sales_analytics_db demo.
Returns (sql, params) where sql is a parameterized query and params is a tuple.
"""

from typing import Tuple, Optional
import re

def normalize(text: str) -> str:
    return text.strip().lower()

def map_to_sql(nl: str) -> Tuple[Optional[str], Optional[Tuple]]:
    """
    Convert a short natural-language request into a parameterized SQL query.
    Returns (sql, params) or (None, None) if no mapping found.
    """
    t = normalize(nl)

    # 1) Count orders by country
    if re.search(r"(count|number).*(orders|purchases).*by country", t) or "orders by country" in t:
        sql = """
        SELECT c.country, COUNT(o.order_id) AS order_count
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.country
        ORDER BY order_count DESC;
        """
        return sql, ()

    # 2) Total revenue by customer
    if re.search(r"(total|sum|revenue).*(by customer|per customer)", t) or "revenue by customer" in t:
        sql = """
        SELECT c.name, SUM(o.amount) AS total_spent
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.name
        ORDER BY total_spent DESC;
        """
        return sql, ()

    # 3) Orders in date range
    m = re.search(r"orders.*from\s+(\d{4}-\d{2}-\d{2}).*to\s+(\d{4}-\d{2}-\d{2})", t)
    if m:
        start, end = m.group(1), m.group(2)
        sql = """
        SELECT order_id, customer_id, product, amount, purchase_date
        FROM orders
        WHERE purchase_date BETWEEN %s AND %s
        ORDER BY purchase_date;
        """
        return sql, (start, end)

    # 4) Top N products by revenue
    m = re.search(r"top\s+(\d+)\s+products", t)
    if m:
        n = int(m.group(1))
        sql = """
        SELECT product, SUM(amount) AS revenue
        FROM orders
        GROUP BY product
        ORDER BY revenue DESC
        LIMIT %s;
        """
        return sql, (n,)

    # 5) Customer lookup by name
    m = re.search(r"(find|get|show).*(customer).*(named|called)\s+([a-zA-Z\s]+)", t)
    if m:
        name = m.group(4).strip()
        sql = "SELECT customer_id, name, country FROM customers WHERE name LIKE %s;"
        return sql, (f"%{name}%",)

    # 6) Fallback: simple SELECT from table
    m = re.match(r"show me all (\w+)", t)
    if m:
        table = m.group(1)
        if table in ("customers", "orders", "products"):
            sql = f"SELECT * FROM {table} LIMIT 100;"
            return sql, ()

    # No mapping found
    return None, None

if __name__ == "__main__":
    examples = [
        "Orders by country",
        "Total revenue by customer",
        "Orders from 2023-01-01 to 2023-06-30",
        "Top 3 products",
        "Find customer named Alice",
        "Show me all customers"
    ]
    for ex in examples:
        q, p = map_to_sql(ex)
        print("NL:", ex)
        print("SQL:", q)
        print("Params:", p)
        print("-" * 40)
