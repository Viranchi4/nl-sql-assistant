import pytest
import nl_sql_assistant.sql.validator as validator
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

def test_schema_validation_rejects_unknown_alias(monkeypatch):
    fake_schema = {
        "categories": {
            "category_id",
            "category_name",
        }
    }

    monkeypatch.setattr(
        validator,
        "get_schema_map",
        lambda: fake_schema,
    )

    query = """
        SELECT c.category_name
        FROM categories cat
    """

    with pytest.raises(
        SQLValidationError,
        match="Unknown table alias",
    ):
        validator.validate_schema_references(query)


def test_schema_validation_rejects_unknown_column(monkeypatch):
    fake_schema = {
        "categories": {
            "category_id",
            "category_name",
        }
    }

    monkeypatch.setattr(
        validator,
        "get_schema_map",
        lambda: fake_schema,
    )

    query = """
        SELECT c.missing_column
        FROM categories c
    """

    with pytest.raises(
        SQLValidationError,
        match="Unknown column",
    ):
        validator.validate_schema_references(query)


def test_schema_validation_accepts_valid_reference(monkeypatch):
    fake_schema = {
        "categories": {
            "category_id",
            "category_name",
        }
    }

    monkeypatch.setattr(
        validator,
        "get_schema_map",
        lambda: fake_schema,
    )

    query = """
        SELECT c.category_name
        FROM categories c
    """

    validator.validate_schema_references(query)