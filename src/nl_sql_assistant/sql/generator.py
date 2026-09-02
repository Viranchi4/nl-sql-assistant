import re

from nl_sql_assistant.llm.ollama_client import generate_text
from nl_sql_assistant.llm.prompts import build_sql_generation_prompt
from nl_sql_assistant.schema import get_database_schema


def clean_sql_response(response: str) -> str:
    """
    Remove Markdown code fences that an LLM may add
    around the generated SQL.
    """

    cleaned = response.strip()

    cleaned = re.sub(
        r"^```(?:sql)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    return cleaned.strip()


def generate_sql(question: str) -> str:
    """
    Convert a natural-language question into SQL
    using the current database schema and local LLM.
    """

    schema = get_database_schema()

    prompt = build_sql_generation_prompt(
        question=question,
        schema=schema,
    )

    response = generate_text(prompt)

    return clean_sql_response(response)