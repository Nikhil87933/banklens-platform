from importlib import import_module
import uuid

framework = import_module(
    "01_bronze.01_bronze_ingestion_framework"
)

config = import_module(
    "00_setup.01_config"
)

audit_utils = import_module(
    "99_utils.audit_utils"
)

batch_id = str(
    uuid.uuid4()
)

for table_name in config.TABLE_NAMES:

    # STATIC + MASTER tables load only once

    if (
        table_name in config.STATIC_TABLES
        or table_name in config.MASTER_TABLES
    ):

        last_day = (
            audit_utils.get_last_successful_day(
                table_name,
                "BRONZE"
            )
        )

        if last_day == 0:

            print(
                f"{table_name} -> Initial Load Day 1"
            )

            framework.ingest_table(
                table_name,
                1,
                batch_id
            )

        else:

            print(
                f"{table_name} -> Already Loaded"
            )

        continue

    # DAILY tables load incrementally

    last_day = (
        audit_utils.get_last_successful_day(
            table_name,
            "BRONZE"
        )
    )

    next_day = last_day + 1

    print(
        f"{table_name} -> Loading Day {next_day}"
    )

    framework.ingest_table(
        table_name,
        next_day,
        batch_id
    )