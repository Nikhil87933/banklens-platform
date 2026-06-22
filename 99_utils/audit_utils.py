from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
    LongType
)

spark = SparkSession.builder.getOrCreate()


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
        StructField("run_id", StringType(), True),
        StructField("pipeline_layer", StringType(), True),
        StructField("table_name", StringType(), True),
        StructField("day_number", IntegerType(), True),
        StructField("source_path", StringType(), True),
        StructField("started_at", TimestampType(), True),
        StructField("completed_at", TimestampType(), True),
        StructField("source_record_count", LongType(), True),
        StructField("target_record_count", LongType(), True),
        StructField("status", StringType(), True),
        StructField("error_message", StringType(), True),
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

    (
        audit_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(
            "banklens.data_quality.pipeline_audit_log"
        )
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
        StructField("columns_renamed", StringType(), True),
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

    (
        schema_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(
            "banklens.data_quality.schema_change_log"
        )
    )

def get_last_successful_day(
    table_name,
    pipeline_layer="BRONZE"
):

    result = spark.sql(
        f"""
        SELECT
            COALESCE(
                MAX(last_successful_day),
                0
            ) AS last_day
        FROM banklens.data_quality.pipeline_control
        WHERE table_name = '{table_name}'
        AND pipeline_layer = '{pipeline_layer}'
        """
    ).collect()

    return result[0]["last_day"]