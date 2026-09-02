import pytest

from nl_sql_assistant.sql.validator import (
    SQLValidationError,
    validate_sql,
)


def test_select_query_is_allowed():
    query = "SELECT * FROM customers"

    validate_sql(query)


def test_delete_query_is_rejected():
    query = "DELETE FROM customers"

    with pytest.raises(SQLValidationError):
        validate_sql(query)


def test_drop_query_is_rejected():
    query = "DROP TABLE customers"

    with pytest.raises(SQLValidationError):
        validate_sql(query)


def test_multiple_statements_are_rejected():
    query = "SELECT * FROM customers; DROP TABLE customers;"

    with pytest.raises(SQLValidationError):
        validate_sql(query)


def test_empty_query_is_rejected():
    query = ""

    with pytest.raises(SQLValidationError):
        validate_sql(query)