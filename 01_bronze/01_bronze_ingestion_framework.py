from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
    LongType
)

from importlib import import_module

spark = SparkSession.builder.getOrCreate()

dbutils = DBUtils(spark)

config = import_module(
    "00_setup.01_config"
)

CATALOG_NAME = config.CATALOG_NAME
BRONZE_SCHEMA = config.BRONZE_SCHEMA
RAW_BASE_PATH = config.RAW_BASE_PATH

STATIC_TABLES = config.STATIC_TABLES
MASTER_TABLES = config.MASTER_TABLES
DAILY_TABLES = config.DAILY_TABLES
TABLE_NAMES = config.TABLE_NAMES


def write_audit_log(
    run_id,
    pipeline_layer,
    table_name,
    day_number,
    source_path,
    started_at,
    completed_at,
    source_record_count,
    target_record_count,
    status,
    error_message
):

    schema = StructType([
        StructField("run_id",               StringType(),    True),
        StructField("pipeline_layer",       StringType(),    True),
        StructField("table_name",           StringType(),    True),
        StructField("day_number",           IntegerType(),   True),
        StructField("source_path",          StringType(),    True),
        StructField("started_at",           TimestampType(), True),
        StructField("completed_at",         TimestampType(), True),
        StructField("source_record_count",  LongType(),      True),
        StructField("target_record_count",  LongType(),      True),
        StructField("status",               StringType(),    True),
        StructField("error_message",        StringType(),    True),
    ])

    audit_df = spark.createDataFrame(
        [
            (
                run_id,
                pipeline_layer,
                table_name,
                day_number,
                source_path,
                started_at,
                completed_at,
                source_record_count,
                target_record_count,
                status,
                error_message
            )
        ],
        schema
    )

    audit_df.write \
        .format("delta") \
        .mode("append") \
        .saveAsTable(
            "banklens.data_quality.pipeline_audit_log"
        )


def write_control_record(
    table_name,
    pipeline_layer,
    day_number
):

    spark.sql(
        f"""
        MERGE INTO banklens.data_quality.pipeline_control t
        USING (
            SELECT
                '{table_name}' AS table_name,
                '{pipeline_layer}' AS pipeline_layer,
                {int(day_number)} AS last_successful_day,
                current_timestamp() AS last_run_at
        ) s
        ON t.table_name = s.table_name
        AND t.pipeline_layer = s.pipeline_layer

        WHEN MATCHED THEN
        UPDATE SET
            t.last_successful_day = s.last_successful_day,
            t.last_run_at = s.last_run_at,
            t.total_runs = t.total_runs + 1

        WHEN NOT MATCHED THEN
        INSERT (
            table_name,
            pipeline_layer,
            last_successful_day,
            last_run_at,
            total_runs
        )
        VALUES (
            s.table_name,
            s.pipeline_layer,
            s.last_successful_day,
            s.last_run_at,
            1
        )
        """
    )
     
def write_schema_change_log(
    table_name,
    day_number,
    current_columns
):

    schema = StructType([
        StructField("table_name", StringType(), True),
        StructField("day_number", IntegerType(), True),
        StructField("detected_at", TimestampType(), True),
        StructField("previous_columns", StringType(), True),
        StructField("current_columns", StringType(), True),
        StructField("columns_added", StringType(), True),
        StructField("columns_removed", StringType(), True),
        StructField("columns_renamed", StringType(), True)
    ])

    schema_df = spark.createDataFrame(
        [
            (
                table_name,
                int(day_number),
                spark.sql(
                    "SELECT current_timestamp()"
                ).collect()[0][0],
                "",
                ",".join(current_columns),
                "",
                "",
                ""
            )
        ],
        schema
    )

    schema_df.write \
        .format("delta") \
        .mode("append") \
        .saveAsTable(
            "banklens.data_quality.schema_change_log"
        )

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

        write_audit_log(
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

    write_schema_change_log(
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

    write_audit_log(
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

    write_control_record(
        table_name=table_name,
        pipeline_layer="BRONZE",
        day_number=day_number
    )
