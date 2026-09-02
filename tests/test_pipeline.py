import pytest

import nl_sql_assistant.pipeline as pipeline
from nl_sql_assistant.sql.validator import SQLValidationError


def test_pipeline_returns_sql_and_results(monkeypatch):
    """
    Test the complete pipeline using fake LLM and database responses.
    """

    fake_sql = "SELECT name FROM customers WHERE country = 'India';"

    fake_results = [
        {"name": "Bob Sharma"},
        {"name": "Diya Patel"},
    ]

    # Replace the real LLM call.
    monkeypatch.setattr(
        pipeline,
        "generate_sql",
        lambda question: fake_sql,
    )

    # Replace the real SQL validation.
    monkeypatch.setattr(
        pipeline,
        "validate_sql",
        lambda sql: None,
    )

    # Replace the real database call.
    monkeypatch.setattr(
        pipeline,
        "execute_query",
        lambda sql: fake_results,
    )

    result = pipeline.run_text_to_sql(
        "Show all customers from India"
    )

    assert result["question"] == "Show all customers from India"
    assert result["sql"] == fake_sql
    assert result["results"] == fake_results


def test_pipeline_rejects_empty_question():
    with pytest.raises(
        ValueError,
        match="Question cannot be empty",
    ):
        pipeline.run_text_to_sql("")


def test_pipeline_does_not_execute_invalid_sql(monkeypatch):
    """
    Verify that database execution never happens
    when SQL validation fails.
    """

    fake_sql = "DELETE FROM customers"

    monkeypatch.setattr(
        pipeline,
        "generate_sql",
        lambda question: fake_sql,
    )

    def reject_sql(sql):
        raise SQLValidationError(
            "Only read-only SELECT queries are allowed."
        )

    monkeypatch.setattr(
        pipeline,
        "validate_sql",
        reject_sql,
    )

    database_was_called = False

    def fake_execute(sql):
        nonlocal database_was_called
        database_was_called = True
        return []

    monkeypatch.setattr(
        pipeline,
        "execute_query",
        fake_execute,
    )

    with pytest.raises(SQLValidationError):
        pipeline.run_text_to_sql(
            "Delete all customers"
        )

    assert database_was_called is False