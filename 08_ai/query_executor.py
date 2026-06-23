def execute_query(spark, sql):

    result_df = spark.sql(sql)

    return result_df