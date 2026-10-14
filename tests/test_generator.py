from nl_sql_assistant.sql.generator import clean_sql_response


def test_plain_sql_is_unchanged():
    response = "SELECT * FROM customers;"

    result = clean_sql_response(response)

    assert result == "SELECT * FROM customers;"


def test_sql_markdown_fence_is_removed():
    response = """```sql
SELECT * FROM customers;
```"""

    result = clean_sql_response(response)

    assert result == "SELECT * FROM customers;"


def test_generic_markdown_fence_is_removed():
    response = """```
SELECT name FROM customers;
```"""

    result = clean_sql_response(response)

    assert result == "SELECT name FROM customers;"