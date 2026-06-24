from pathlib import Path
from intent_router import get_schema_files
from ollama_client import ask_ollama


def load_schemas(schema_files):

    schema_dir = (
        Path(__file__).parent
        / "schemas"
    )

    schemas = []

    for file_name in schema_files:

        with open(
            schema_dir / file_name,
            "r"
        ) as f:

            schemas.append(
                f.read()
            )

    return "\n\n".join(
        schemas
    )


def build_prompt(question):

    schema_files = get_schema_files(
        question
    )

    print(
        "Schemas Used:",
        schema_files
    )

    schema = load_schemas(
        schema_files
    )

    prompt = f"""
    You are an expert Databricks SQL developer.

    Rules:
    - Return SQL only.
    - Do not explain.
    - Do not use markdown.
    - Use only tables and columns provided.
    - Never invent tables.
    - Never invent columns.

    Business Rules:
    - If user asks "how many", use COUNT() or SUM().
    - If user asks "total", use SUM().
    - If user asks "average", use AVG().
    - If user asks "highest", use MAX().
    - If user asks "lowest", use MIN().
    - Return a single aggregated answer whenever possible.

    Rules for Aggregated Tables:

    If a table already contains aggregated metrics such as:
    - loan_count
    - customer_count
    - total_balance
    - total_outstanding_balance

    and the user asks for:
    - total
    - overall total
    - how many

    then use SUM() on the metric column.

    Available Schemas:

    {schema}

    Examples:

    Question:
    How many loans do we have?

    SQL:
    SELECT SUM(loan_count)
    FROM banklens.gold.gld_loan_portfolio

    Question:
    What is the total outstanding loan balance?

    SQL:
    SELECT SUM(total_outstanding_balance)
    FROM banklens.gold.gld_loan_portfolio

    Question:
    How many HIGH risk customers do we have?

    SQL:
    SELECT COUNT(*)
    FROM banklens.ml.churn_predictions
    WHERE risk_band = 'HIGH'

    Question:

    {question}
    """
    return prompt


def generate_sql(question):

    prompt = build_prompt(
        question
    )

    sql = ask_ollama(
        prompt
    )

    return sql.strip()


if __name__ == "__main__":

    sql = generate_sql(
        "How many HIGH risk customers do we have?"
    )

    print(sql)