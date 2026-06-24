from query_executor import execute_query
from pathlib import Path

TABLES = [
    "banklens.ml.churn_predictions",
    "banklens.gold.gold_customer_360",
    "banklens.gold.gld_churn_features",
    "banklens.gold.gld_loan_portfolio",
    "banklens.gold.gld_executive_kpis"
]

schema_dir = Path("schemas")
schema_dir.mkdir(exist_ok=True)

for table in TABLES:

    rows = execute_query(
        f"DESCRIBE {table}"
    )

    file_name = table.split(".")[-1] + ".txt"

    with open(schema_dir / file_name, "w") as f:

        f.write(f"Table: {table}\n\n")

        for row in rows:
            f.write(
                f"{row.col_name} {row.data_type}\n"
            )

    print(f"Created {file_name}")