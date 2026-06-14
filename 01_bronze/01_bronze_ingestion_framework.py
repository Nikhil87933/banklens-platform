from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from importlib import import_module

spark = SparkSession.builder.getOrCreate()

dbutils = DBUtils(spark)

config = import_module(
    "00_setup.01_config"
)

audit_utils = import_module(
    "99_utils.audit_utils"
)

CATALOG_NAME = config.CATALOG_NAME
BRONZE_SCHEMA = config.BRONZE_SCHEMA
RAW_BASE_PATH = config.RAW_BASE_PATH

STATIC_TABLES = config.STATIC_TABLES
MASTER_TABLES = config.MASTER_TABLES
DAILY_TABLES = config.DAILY_TABLES
TABLE_NAMES = config.TABLE_NAMES


def is_table_expected(
    table_name: str,
    day_number: int
) -> bool:

    if table_name in STATIC_TABLES:
        return day_number == 1

    if table_name in MASTER_TABLES:
        return day_number == 1

    if table_name in DAILY_TABLES:
        return True

    return False


def build_source_path(
    table_name: str,
    day_number: int
) -> str:

    return (
        f"{RAW_BASE_PATH}/"
        f"day_{day_number}/"
        f"{table_name}.csv"
    )


def file_exists(
    path: str
) -> bool:

    try:
        dbutils.fs.ls(path)

        print(
            f"FOUND: {path}"
        )

        return True

    except Exception as e:

        print(
            f"ERROR: {e}"
        )

        return False


def ingest_table(
    table_name: str,
    day_number: int,
    batch_id: str
):

    print(
        f"Ingesting {table_name}"
        f" for day {day_number}"
    )

    started_at = spark.sql(
        "SELECT current_timestamp()"
    ).collect()[0][0]

    source_path = build_source_path(
        table_name,
        day_number
    )

    print(
        f"Source Path = {source_path}"
    )

    if not is_table_expected(
        table_name,
        day_number
    ):
        print(
            f"Skipping {table_name}"
        )
        return

    if not file_exists(
        source_path
    ):

        audit_utils.write_audit_log(
            run_id=batch_id,
            pipeline_layer="BRONZE",
            table_name=table_name,
            day_number=day_number,
            source_path=source_path,
            started_at=started_at,
            completed_at=started_at,
            source_record_count=0,
            target_record_count=0,
            status="FAILED",
            error_message="File not found"
        )

        print(
            f"File not found: {source_path}"
        )

        return

    df = (
        spark.read
        .option("header", "true")
        .option("delimiter", "|")
        .option("inferSchema", "false")
        .option(
            "rescuedDataColumn",
            "_rescued_data"
        )
        .csv(source_path)
    )

    source_columns = df.columns

    audit_utils.write_schema_change_log(
        table_name=table_name,
        day_number=day_number,
        current_columns=source_columns
    )

    print(
        f"Columns found = "
        f"{len(source_columns)}"
    )

    source_count = df.count()

    print(
        f"Rows read = "
        f"{source_count}"
    )

    df = (
        df
        .withColumn(
            "_source_file",
            F.col("_metadata.file_path")
        )
        .withColumn(
            "_ingestion_timestamp",
            F.current_timestamp()
        )
        .withColumn(
            "_day_number",
            F.lit(day_number)
        )
        .withColumn(
            "_batch_id",
            F.lit(batch_id)
        )
    )

    print(
        "Metadata columns added"
    )

    df = df.withColumn(
        "_row_hash",
        F.sha2(
            F.concat_ws(
                "||",
                *[
                    F.coalesce(
                        F.col(column_name),
                        F.lit("")
                    )
                    for column_name in source_columns
                ]
            ),
            256
        )
    )

    print(
        "Row hash added"
    )

    target_table = (
        f"{CATALOG_NAME}."
        f"{BRONZE_SCHEMA}."
        f"brz_{table_name}"
    )

    df.write \
        .format("delta") \
        .mode("append") \
        .option(
            "mergeSchema",
            "true"
        ) \
        .saveAsTable(
            target_table
        )

    print(
        f"Written to {target_table}"
    )

    completed_at = spark.sql(
        "SELECT current_timestamp()"
    ).collect()[0][0]

    audit_utils.write_audit_log(
        run_id=batch_id,
        pipeline_layer="BRONZE",
        table_name=table_name,
        day_number=day_number,
        source_path=source_path,
        started_at=started_at,
        completed_at=completed_at,
        source_record_count=source_count,
        target_record_count=source_count,
        status="SUCCESS",
        error_message=""
    )

    audit_utils.write_control_record(
        table_name=table_name,
        pipeline_layer="BRONZE",
        day_number=day_number
    )