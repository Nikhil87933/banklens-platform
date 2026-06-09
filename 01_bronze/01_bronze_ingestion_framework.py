from pyspark.sql import functions as F

from importlib import import_module

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
        return True

    except Exception:
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

    print(
        f"Columns found = "
        f"{len(source_columns)}"
    )

    source_count = df.count()

    print(
        f"Rows read = "
        f"{source_count}"
    )