import subprocess
from pathlib import Path


MODEL_NAME = "qwen2.5:7b"


def load_schema():

    schema_path = (
        Path(__file__).parent
        / "schemas"
        / "churn_predictions.txt"
    )

    with open(schema_path, "r") as f:
        return f.read()


def build_prompt(question):

    schema = load_schema()

    prompt = f"""
You are generating Databricks SQL.

Rules:
- Return SQL only.
- Use only tables and columns provided.
- Never invent column names.
- Never explain.
- Never use markdown.

Schema:

{schema}

Question:

{question}
"""

    return prompt


def generate_sql(question):

    prompt = build_prompt(question)

    result = subprocess.run(
        [
            "ollama",
            "run",
            MODEL_NAME
        ],
        input=prompt,
        text=True,
        capture_output=True
    )

    sql = result.stdout.strip()

    return sql


if __name__ == "__main__":

    question = (
        "How many HIGH risk customers do we have?"
    )

    sql = generate_sql(question)

    print(sql)