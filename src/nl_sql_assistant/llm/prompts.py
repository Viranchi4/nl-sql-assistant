def build_sql_generation_prompt(question: str, schema: str) -> str:
    """
    Build a schema-aware prompt for converting
    natural language into MySQL SQL.
    """

    return f"""
You are an expert MySQL Text-to-SQL assistant.

Convert the user's natural-language question into one valid MySQL query.

DATABASE SCHEMA:
{schema}

RULES:
1. Use only tables and columns present in the database schema.
2. Do not invent table names or column names.
3. Use the foreign-key relationships shown in the schema when joins are needed.
4. Generate read-only SQL only.
5. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE,
   CREATE, REPLACE, or any other statement that modifies the database.
6. Use MySQL-compatible syntax.
7. For revenue or spending calculations, use the historical order item price:
   order_items.quantity * order_items.unit_price.
8. Return only the SQL query.
9. Do not include explanations.
10. Do not include Markdown code fences.

USER QUESTION:
{question}

SQL:
""".strip()