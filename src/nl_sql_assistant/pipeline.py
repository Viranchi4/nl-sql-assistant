from nl_sql_assistant.sql.executor import execute_query
from nl_sql_assistant.sql.generator import generate_sql
from nl_sql_assistant.sql.validator import validate_sql


def run_text_to_sql(question: str) -> dict:
    """
    Convert a natural-language question into SQL,
    validate the generated query, execute it,
    and return the results.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Generate SQL using the local LLM.
    sql = generate_sql(question)

    # Step 2: Validate before allowing database execution.
    validate_sql(sql)

    # Step 3: Execute only after validation succeeds.
    results = execute_query(sql)

    return {
        "question": question,
        "sql": sql,
        "results": results,
    }