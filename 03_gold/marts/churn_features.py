from pyspark.sql import functions as F


def build_churn_features(spark):

    customer_df = spark.table(
        "banklens.silver.slv_customer_master"
    )

    digital_df = spark.table(
        "banklens.silver.slv_digital_activity"
    )

    support_df = spark.table(
        "banklens.silver.slv_support_tickets"
    )

    product_df = spark.table(
        "banklens.silver.slv_product_holdings"
    )

    account_df = spark.table(
        "banklens.silver.slv_account_master"
    )

    digital_features = (
        digital_df
        .groupBy("customer_id")
        .agg(
            F.count("*").alias(
                "digital_sessions"
            )
        )
    )

    support_features = (
        support_df
        .groupBy("customer_id")
        .agg(
            F.count("*").alias(
                "support_ticket_count"
            )
        )
    )

    product_features = (
        product_df
        .groupBy("customer_id")
        .agg(
            F.count("*").alias(
                "product_count"
            )
        )
    )

    account_features = (
        account_df
        .groupBy("customer_id")
        .agg(
            F.countDistinct(
                "account_id"
            ).alias(
                "total_accounts"
            ),

            F.sum(
                "current_balance"
            ).alias(
                "total_balance"
            )
        )
    )

    churn_df = (
        customer_df
        .select(
            "customer_id",
            "customer_type",
            "customer_since_date",
            "is_churn",
            "nps_score"
        )
        .join(
            digital_features,
            "customer_id",
            "left"
        )
        .join(
            support_features,
            "customer_id",
            "left"
        )
        .join(
            product_features,
            "customer_id",
            "left"
        )

        .join(
            account_features,
            "customer_id",
            "left"
        )
        .withColumn(
            "tenure_days",
            F.datediff(
                F.current_date(),
                F.col("customer_since_date")
            )
        )
        .fillna(0)
    )

    return churn_df