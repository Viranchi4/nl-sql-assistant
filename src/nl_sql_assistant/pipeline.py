import mysql.connector

from nl_sql_assistant.sql.executor import execute_query
from nl_sql_assistant.sql.generator import correct_sql, generate_sql
from nl_sql_assistant.sql.validator import validate_sql


MAX_CORRECTION_ATTEMPTS = 1


def run_text_to_sql(question: str) -> dict:
    """
    Convert a natural-language question into SQL,
    validate it, execute it, and attempt one correction
    if MySQL reports an execution error.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    original_sql = generate_sql(question)

    validate_sql(original_sql)

    sql = original_sql
    corrected = False

    try:
        results = execute_query(sql)

    except mysql.connector.Error as error:
        if MAX_CORRECTION_ATTEMPTS < 1:
            raise

        sql = correct_sql(
            question=question,
            failed_sql=original_sql,
            error_message=str(error),
        )

        # The corrected SQL must pass the same safety
        # validation before it can reach the database.
        validate_sql(sql)

        results = execute_query(sql)
        corrected = True

    return {
        "question": question,
        "sql": sql,
        "original_sql": original_sql,
        "corrected": corrected,
        "results": results,
    }