from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from importlib import import_module

spark = SparkSession.builder.getOrCreate()

config = import_module(
    "00_setup.01_config"
)

audit_utils = import_module(
    "99_utils.audit_utils"
)

CATALOG_NAME = config.CATALOG_NAME

BRONZE_SCHEMA = config.BRONZE_SCHEMA
SILVER_SCHEMA = config.SILVER_SCHEMA


def read_bronze_table(
    table_name: str
):

    source_table = (
        f"{CATALOG_NAME}."
        f"{BRONZE_SCHEMA}."
        f"brz_{table_name}"
    )

    print(
        f"Reading {source_table}"
    )

    df = spark.table(
        source_table
    )

    return df


def deduplicate_records(
    df
):

    before_count = df.count()

    df = df.dropDuplicates(
        ["_row_hash"]
    )

    after_count = df.count()

    duplicates_removed = (
        before_count - after_count
    )

    print(
        f"Duplicates removed = "
        f"{duplicates_removed}"
    )

    return (
        df,
        before_count,
        after_count,
        duplicates_removed
    )


def write_silver_table(
    df,
    table_name: str
):

    target_table = (
        f"{CATALOG_NAME}."
        f"{SILVER_SCHEMA}."
        f"slv_{table_name}"
    )

    print(
        f"Writing {target_table}"
    )

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option(
            "overwriteSchema",
            "true"
        )
        .saveAsTable(
            target_table
        )
    )

    print(
        f"Written to {target_table}"
    )


def process_table(
    table_name: str,
    run_id: str
):

    print(
        f"Processing {table_name}"
    )

    started_at = spark.sql(
        "SELECT current_timestamp()"
    ).collect()[0][0]

    try:

        df = read_bronze_table(
            table_name
        )

        (
            df,
            source_count,
            target_count,
            duplicates_removed
        ) = deduplicate_records(
            df
        )

        write_silver_table(
            df,
            table_name
        )

        completed_at = spark.sql(
            "SELECT current_timestamp()"
        ).collect()[0][0]

        audit_utils.write_audit_log(
            run_id=run_id,
            pipeline_layer="SILVER",
            table_name=table_name,
            day_number=0,
            source_path="BRONZE_TABLE",
            started_at=started_at,
            completed_at=completed_at,
            source_record_count=source_count,
            target_record_count=target_count,
            status="SUCCESS",
            error_message=""
        )

        print(
            f"Source Rows = "
            f"{source_count}"
        )

        print(
            f"Target Rows = "
            f"{target_count}"
        )

        print(
            f"Duplicates Removed = "
            f"{duplicates_removed}"
        )

        print(
            f"Completed {table_name}"
        )

    except Exception as e:

        completed_at = spark.sql(
            "SELECT current_timestamp()"
        ).collect()[0][0]

        audit_utils.write_audit_log(
            run_id=run_id,
            pipeline_layer="SILVER",
            table_name=table_name,
            day_number=0,
            source_path="BRONZE_TABLE",
            started_at=started_at,
            completed_at=completed_at,
            source_record_count=0,
            target_record_count=0,
            status="FAILED",
            error_message=str(e)
        )

        raise e