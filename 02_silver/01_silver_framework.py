from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from importlib import import_module

spark = SparkSession.builder.getOrCreate()

config = import_module(
    "00_setup.01_config"
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

    print(
        f"Duplicates removed = "
        f"{before_count - after_count}"
    )

    return df


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
    table_name: str
):

    print(
        f"Processing {table_name}"
    )

    df = read_bronze_table(
        table_name
    )

    df = deduplicate_records(
        df
    )

    write_silver_table(
        df,
        table_name
    )

    print(
        f"Completed {table_name}"
    )