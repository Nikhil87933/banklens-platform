from importlib import import_module
import uuid

framework = import_module(
    "02_silver.01_silver_framework"
)

run_id = str(
    uuid.uuid4()
)

print(
    f"Run ID = {run_id}"
)

TABLES = [
    "merchant_reference"
]

for table_name in TABLES:

    framework.process_table(
        table_name,
        run_id
    )

print(
    "Silver load complete"
)