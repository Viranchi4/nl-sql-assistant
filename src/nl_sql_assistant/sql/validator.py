import sqlglot
from sqlglot import exp


class SQLValidationError(ValueError):
    """Raised when generated SQL is unsafe or invalid."""


def validate_sql(query: str) -> None:
    """
    Validate that SQL is syntactically valid and read-only.

    Raises:
        SQLValidationError: if the query is invalid or unsafe.
    """

    if not query or not query.strip():
        raise SQLValidationError("SQL query is empty.")

    try:
        statements = sqlglot.parse(
            query,
            read="mysql",
        )
    except sqlglot.errors.ParseError as error:
        raise SQLValidationError(
            f"Invalid SQL syntax: {error}"
        ) from error

    # We allow exactly one SQL statement.
    if len(statements) != 1:
        raise SQLValidationError(
            "Only one SQL statement is allowed."
        )

    statement = statements[0]

    # SQLGlot represents read-only SELECT-style statements
    # as Query expressions.
    if not isinstance(statement, exp.Query):
        raise SQLValidationError(
            "Only read-only SELECT queries are allowed."
        )