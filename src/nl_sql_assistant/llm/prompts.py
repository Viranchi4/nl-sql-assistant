def build_sql_generation_prompt(question: str, schema: str, value_context: str) -> str:
    """
    Build a schema-aware prompt for converting
    natural language into MySQL SQL.
    """

    return f"""
You are an expert MySQL Text-to-SQL assistant.

Convert the user's natural-language question into one valid MySQL query.

DATABASE SCHEMA:
{schema}

KNOWN DATABASE VALUES:
{value_context}

RULES:
1. Use only tables and columns present in the database schema.
2. Do not invent table names or column names.
3. Use the foreign-key relationships shown in the schema when joins are needed.
4. When filtering categorical/text values, prefer exact values from
   KNOWN DATABASE VALUES instead of inventing or singularizing values.
5. Generate read-only SQL only.
6. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE,
   CREATE, REPLACE, or any other statement that modifies the database.
7. Use MySQL-compatible syntax.
8. For revenue or spending calculations, use the historical order item price:
   order_items.quantity * order_items.unit_price.
9. Determine the level of aggregation requested by the user before writing the SQL query.
10. When a metric belongs to a parent entity but its values are stored across multiple child rows,
    first aggregate the child rows to the parent entity level, then perform the requested aggregate.
11. Do not calculate the average of individual line-item values when 
    the user asks for the average value of the parent transaction.
12. In this schema, one order can contain multiple order_items. 
    The total value of an order is the sum of:
    order_items.quantity * order_items.unit_price
    for all order_items belonging to that order.
13. Return only the SQL query.
14. Do not include explanations.
15. Do not include Markdown code fences.

EXAMPLE OF AGGREGATION REASONING:

Question:
What is the average value of an order?

Reasoning:
An order can contain multiple rows in order_items.
First calculate the total value of each order by summing
quantity * unit_price for that order.
Then calculate the average of those order totals.

SQL:
SELECT AVG(order_total) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(quantity * unit_price) AS order_total
    FROM order_items
    GROUP BY order_id
) AS order_totals;

USER QUESTION:
{question}

SQL:
""".strip()

def build_sql_correction_prompt(
    question: str,
    schema: str,
    value_context: str,
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

KNOWN DATABASE VALUES:
{value_context}

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
4. When filtering categorical/text values, use exact matching values from
   KNOWN DATABASE VALUES whenever relevant.
5. Every JOIN must follow a foreign-key relationship explicitly shown
   in the database schema.
6. Never join two columns merely because they have similar names,
   compatible data types, or similar numeric values.
7. Include every intermediate table required by the foreign-key path.
8. Generate read-only SQL only.
9. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER,
   TRUNCATE, CREATE, or REPLACE.
10. For revenue or spending calculations, use:
    order_items.quantity * order_items.unit_price.
11. Ensure the corrected query still answers the ORIGINAL USER QUESTION,
    not just the database error.
12. Return only the corrected SQL query.
13. Do not include explanations.
14. Do not include Markdown code fences.

CORRECTED SQL:
""".strip()