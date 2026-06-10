from importlib import import_module
import uuid

framework = import_module(
    "01_bronze.01_bronze_ingestion_framework"
)

config = import_module(
    "00_setup.01_config"
)

batch_id = str(
    uuid.uuid4()
)

for table_name in config.TABLE_NAMES:

    framework.ingest_table(
        table_name,
        1,
        batch_id
    )

print(
    "Bronze load complete"
)
