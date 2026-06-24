from sql_generator import generate_sql
from sql_validator import validate_sql
from query_executor import execute_query
from summary_generator import summarize_result
from ollama_client import ask_ollama


def main():

    question = input(
        "Ask BankLens: "
    )

    sql = generate_sql(
        question
    )

    print("\nGenerated SQL:\n")
    print(sql)

    validate_sql(sql)

    try:

        rows = execute_query(sql)

    except Exception as e:

        print("\nSQL Failed")
        print(str(e))

        repair_prompt = f"""
    You are a Databricks SQL expert.

    The following SQL failed.

    SQL:
    {sql}

    Error:
    {str(e)}

    Return corrected SQL only.
    """

        fixed_sql = ask_ollama(
            repair_prompt
        )

        fixed_sql = fixed_sql.strip()

        print("\nCorrected SQL:\n")
        print(fixed_sql)

        rows = execute_query(
            fixed_sql
        )

        sql = fixed_sql
    summary = summarize_result(
        question,
        sql,
        rows
    )

    print("\nResult:\n")

    for row in rows:
        print(row)

    print("\nAI Summary:\n")
    print(summary)


if __name__ == "__main__":
    main()