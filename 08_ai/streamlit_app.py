import streamlit as st

from sql_generator import generate_sql
from sql_validator import validate_sql
from query_executor import execute_query
from summary_generator import summarize_result

st.set_page_config(
    page_title="BankLens AI Copilot",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 BankLens AI Copilot")

question = st.text_input(
    "Ask a business question"
)

if st.button("Ask"):

    try:

        sql = generate_sql(
            question
        )

        validate_sql(
            sql
        )

        rows = execute_query(
            sql
        )

        summary = summarize_result(
            question,
            sql,
            rows
        )

        st.subheader(
            "Generated SQL"
        )

        st.code(
            sql,
            language="sql"
        )

        st.subheader(
            "Result"
        )

        st.write(
            rows
        )

        st.subheader(
            "AI Summary"
        )

        st.write(
            summary
        )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )