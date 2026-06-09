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