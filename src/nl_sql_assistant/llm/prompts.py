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

def build_sql_correction_prompt(
    question: str,
    schema: str,
    failed_sql: str,
    error_message: str,
) -> str:
    """
    Build a prompt that asks the LLM to correct
    a SQL query that failed during execution.
    """

    return f"""
You are an expert MySQL Text-to-SQL assistant.

A previously generated SQL query failed.

Correct the query using the database schema and database error below.

DATABASE SCHEMA:
{schema}

ORIGINAL USER QUESTION:
{question}

FAILED SQL:
{failed_sql}

DATABASE ERROR:
{error_message}

RULES:
1. Rebuild the complete SQL query when necessary instead of making
   only a minimal textual fix.
2. Use only tables and columns present in the database schema.
3. Do not invent tables or columns.
4. Every JOIN must follow a foreign-key relationship explicitly shown
   in the database schema.
5. Never join two columns merely because they have similar names,
   compatible data types, or similar numeric values.
6. Include every intermediate table required by the foreign-key path.
7. Generate read-only SQL only.
8. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, or REPLACE.
9. For revenue or spending calculations, use:
   order_items.quantity * order_items.unit_price.
10. Ensure the corrected query still answers the ORIGINAL USER QUESTION,
    not just the database error.
11. Return only the corrected SQL query.
12. Do not include explanations.
13. Do not include Markdown code fences.

CORRECTED SQL:
""".strip()