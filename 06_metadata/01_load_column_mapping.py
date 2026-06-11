from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.getOrCreate()

df = (
    spark.read
    .option("header", "true")
    .csv(
        "file:/Workspace/Users/chamlenikhil1@gmail.com/banklens-platform/00_setup/metadata/column_mapping.csv"
    )
)

df = df.withColumn(
    "loaded_at",
    F.current_timestamp()
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
        "banklens.metadata.column_mapping"
    )
)

print(
    "Column mapping loaded successfully"
)