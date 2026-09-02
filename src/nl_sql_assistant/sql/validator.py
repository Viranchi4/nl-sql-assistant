import sqlglot
from sqlglot import exp

from nl_sql_assistant.schema import get_schema_map


class SQLValidationError(ValueError):
    """Raised when generated SQL is unsafe or invalid."""

class SQLSchemaValidationError(SQLValidationError):
    """
    Raised when SQL references tables, aliases,
    or columns that do not match the database schema.
    """


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

def validate_schema_references(query: str) -> None:
    """
    Validate table names, table aliases, and qualified column
    references against the actual database schema.

    Example:
        SELECT c.category_name
        FROM categories cat

    will be rejected because alias 'c' does not exist.
    """

    try:
        statement = sqlglot.parse_one(
            query,
            read="mysql",
        )
    except sqlglot.errors.ParseError as error:
        raise SQLSchemaValidationError(
            f"Invalid SQL syntax: {error}"
        ) from error

    schema_map = get_schema_map()

    alias_to_table = {}

    # ---------------------------------------------------------
    # Validate table names and build alias lookup.
    # ---------------------------------------------------------
    for table in statement.find_all(exp.Table):
        table_name = table.name

        if table_name not in schema_map:
            raise SQLSchemaValidationError(
                f"Unknown table: {table_name}"
            )

        alias = table.alias_or_name

        alias_to_table[alias] = table_name

    # ---------------------------------------------------------
    # Validate qualified columns such as:
    #
    # c.category_name
    # oi.quantity
    # ---------------------------------------------------------
    for column in statement.find_all(exp.Column):
        column_name = column.name
        table_alias = column.table

        # For now, only validate qualified columns.
        # We will handle unqualified columns separately later.
        if not table_alias:
            continue

        if table_alias not in alias_to_table:
            raise SQLSchemaValidationError(
                f"Unknown table alias: {table_alias}"
            )

        real_table_name = alias_to_table[table_alias]

        if column_name not in schema_map[real_table_name]:
            raise SQLSchemaValidationError(
                f"Unknown column '{column_name}' "
                f"for table '{real_table_name}'"
            )