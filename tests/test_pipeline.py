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

def test_pipeline_corrects_sql_after_database_error(monkeypatch):
    """
    If the first SQL query fails in MySQL,
    the pipeline should correct it and retry once.
    """

    import mysql.connector

    original_sql = (
        "SELECT c.category_name "
        "FROM categories cat LIMIT 1;"
    )

    corrected_sql = (
        "SELECT cat.category_name "
        "FROM categories cat LIMIT 1;"
    )

    expected_results = [
        {"category_name": "Laptops"},
    ]

    monkeypatch.setattr(
        pipeline,
        "generate_sql",
        lambda question: original_sql,
    )

    monkeypatch.setattr(
        pipeline,
        "validate_sql",
        lambda sql: None,
    )

    monkeypatch.setattr(
        pipeline,
        "correct_sql",
        lambda question, failed_sql, error_message: corrected_sql,
    )

    execution_count = 0

    def fake_execute(sql):
        nonlocal execution_count
        execution_count += 1

        if execution_count == 1:
            raise mysql.connector.Error(
                "Unknown column c.category_name"
            )

        return expected_results

    monkeypatch.setattr(
        pipeline,
        "execute_query",
        fake_execute,
    )

    result = pipeline.run_text_to_sql(
        "Show the highest revenue product category"
    )

    assert execution_count == 2
    assert result["original_sql"] == original_sql
    assert result["sql"] == corrected_sql
    assert result["corrected"] is True
    assert result["results"] == expected_results

def test_pipeline_marks_successful_first_attempt_as_not_corrected(
    monkeypatch,
):
    fake_sql = "SELECT * FROM customers;"
    fake_results = [{"customer_id": 1}]

    monkeypatch.setattr(
        pipeline,
        "generate_sql",
        lambda question: fake_sql,
    )

    monkeypatch.setattr(
        pipeline,
        "validate_sql",
        lambda sql: None,
    )

    monkeypatch.setattr(
        pipeline,
        "execute_query",
        lambda sql: fake_results,
    )

    result = pipeline.run_text_to_sql(
        "Show all customers"
    )

    assert result["sql"] == fake_sql
    assert result["original_sql"] == fake_sql
    assert result["corrected"] is False
    assert result["results"] == fake_results