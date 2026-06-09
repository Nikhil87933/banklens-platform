import uuid

from importlib import import_module

framework = import_module(
    "01_bronze.01_bronze_ingestion_framework"
)

batch_id = str(
    uuid.uuid4()
)

framework.ingest_table(
    "customer_master",
    1,
    batch_id
)