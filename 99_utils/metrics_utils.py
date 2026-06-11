from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    LongType,
    TimestampType
)

spark = SparkSession.builder.getOrCreate()


def write_pipeline_metrics(
    run_id,
    pipeline_layer,
    table_name,
    source_record_count,
    target_record_count,
    duplicates_removed
):

    schema = StructType([
        StructField(
            "run_id",
            StringType(),
            True
        ),
        StructField(
            "pipeline_layer",
            StringType(),
            True
        ),
        StructField(
            "table_name",
            StringType(),
            True
        ),
        StructField(
            "source_record_count",
            LongType(),
            True
        ),
        StructField(
            "target_record_count",
            LongType(),
            True
        ),
        StructField(
            "duplicates_removed",
            LongType(),
            True
        ),
        StructField(
            "metric_timestamp",
            TimestampType(),
            True
        )
    ])

    metric_df = spark.createDataFrame(
        [
            (
                run_id,
                pipeline_layer,
                table_name,
                source_record_count,
                target_record_count,
                duplicates_removed,
                spark.sql(
                    "SELECT current_timestamp()"
                ).collect()[0][0]
            )
        ],
        schema
    )

    (
        metric_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(
            "banklens.data_quality.pipeline_metrics"
        )
    )