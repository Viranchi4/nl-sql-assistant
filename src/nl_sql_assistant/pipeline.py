import mysql.connector

from nl_sql_assistant.sql.executor import execute_query
from nl_sql_assistant.sql.generator import correct_sql, generate_sql
from nl_sql_assistant.sql.validator import (
    SQLSchemaValidationError,
    validate_schema_references,
    validate_sql,
)


MAX_CORRECTION_ATTEMPTS = 2


def run_text_to_sql(question: str) -> dict:
    """
    Convert a natural-language question into SQL,
    validate it, execute it, and retry correction
    when MySQL reports an execution error.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    original_sql = generate_sql(question)

    sql = original_sql
    correction_attempts = 0

    while True:
        # Safety validation always runs first.
        # Unsafe SQL is rejected immediately and is NOT corrected.
        validate_sql(sql)

        try:
            # Validate schema references before MySQL execution.
            validate_schema_references(sql)

            results = execute_query(sql)
            break

        except (
            SQLSchemaValidationError,
            mysql.connector.Error,
        ) as error:
            if correction_attempts >= MAX_CORRECTION_ATTEMPTS:
                raise

            sql = correct_sql(
                question=question,
                failed_sql=sql,
                error_message=str(error),
            )

            correction_attempts += 1
    return {
        "question": question,
        "sql": sql,
        "original_sql": original_sql,
        "corrected": correction_attempts > 0,
        "correction_attempts": correction_attempts,
        "results": results,
    }