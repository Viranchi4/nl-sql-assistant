import streamlit as st
from nl_sql_assistant.pipeline import run_text_to_sql
from nl_sql_assistant.llm.ollama_client import DEFAULT_MODEL
from nl_sql_assistant.schema import get_schema_map

EXAMPLE_QUESTIONS = [
    "Show the top 5 customers by total spending",
    "Which product generated the highest revenue?",
    "What is the average order value?",
    "How many customers are from India?",
    "Which product category generated the highest revenue from customers in India?",
]

st.set_page_config(
    page_title="NL-SQL Assistant",
    page_icon="🧠",
    layout="wide",
)

with st.sidebar:
    st.header("Runtime")

    st.write("**Local LLM**")
    st.code(DEFAULT_MODEL)

    st.caption(
        "Model served locally through Ollama."
    )

    st.divider()

    st.write("**Example Questions**")

    example_question = st.selectbox(
        "Choose an example",
        options=[""] + EXAMPLE_QUESTIONS,
        format_func=lambda value: (
            "Select an example..."
            if value == ""
            else value
        ),
    )

    st.divider()

    st.write("**Database Schema**")

    try:
        schema_map = get_schema_map()

        with st.expander("View tables and columns"):
            for table_name, columns in schema_map.items():
                st.markdown(f"**{table_name}**")

                for column in sorted(columns):
                    st.write(f"- {column}")

    except Exception as error:
        st.caption(
            "Database schema could not be loaded."
        )

st.title("🧠 Natural Language to SQL Assistant")

st.write(
    "Ask questions about a MySQL database using natural language."
)

st.info(
    "The application uses a local LLM through Ollama "
    "to generate and validate SQL queries."
)

with st.expander("⚙️ How it works"):
    st.markdown(
        """
1. Your natural-language question is combined with the live MySQL schema
   and known categorical database values.
2. A local Qwen2.5-Coder model generates a MySQL query through Ollama.
3. The SQL is parsed and validated before execution.
4. Only safe, read-only queries are allowed.
5. Valid SQL is executed against the MySQL database and the results are displayed.
6. If validation or execution fails, the pipeline can make bounded correction attempts.
        """
    )

st.subheader("Ask a Question")

with st.form("nl_sql_form"):
    question = st.text_input(
        "Natural-language question",
        value=example_question,
        placeholder="e.g. Show the top 5 customers by total spending",
    )

    submitted = st.form_submit_button(
        "Generate SQL",
        type="primary",
    )


if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Generating SQL and querying the database..."):
                result = run_text_to_sql(question)

            st.subheader("Generated SQL")
            st.code(result["sql"], language="sql")

            st.subheader("Results")

            row_count = len(result["results"])

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Rows returned",
                    value=row_count,
                )

            with col2:
                if result["corrected"]:
                    st.metric(
                        label="SQL correction",
                        value=f"{result['correction_attempts']} attempt(s)",
                    )
                else:
                    st.metric(
                        label="SQL correction",
                        value="Not needed",
                    )


            if result["results"]:
                st.dataframe(
                    result["results"],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info(
                    "The query executed successfully but returned no rows."
                )
            
        except Exception as error:
            st.error(str(error))