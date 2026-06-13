from pyspark.sql import functions as F


def build_fraud_features(spark):

    txn_df = spark.table(
        "banklens.silver.slv_transaction_fact"
    )

    card_df = spark.table(
        "banklens.silver.slv_card_transaction_fact"
    )

    device_df = spark.table(
        "banklens.silver.slv_device_events"
    )

    txn_features = (
        txn_df
        .groupBy("customer_id")
        .agg(
            F.count("*").alias(
                "total_transactions"
            ),

            F.sum(
                F.when(
                    F.col("is_flagged") == True,
                    1
                ).otherwise(0)
            ).alias(
                "flagged_transactions"
            )
        )
    )

    card_features = (
        card_df
        .groupBy("customer_id")
        .agg(
            F.sum(
                F.when(
                    F.col("is_international") == True,
                    1
                ).otherwise(0)
            ).alias(
                "international_txns"
            ),

            F.sum(
                F.when(
                    F.col("is_disputed") == True,
                    1
                ).otherwise(0)
            ).alias(
                "disputed_txns"
            )
        )
    )

    device_features = (
        device_df
        .groupBy("customer_id")
        .agg(
            F.sum(
                F.when(
                    F.col("is_vpn") == True,
                    1
                ).otherwise(0)
            ).alias(
                "vpn_events"
            ),

            F.sum(
                "failed_auth_count"
            ).alias(
                "failed_auth_attempts"
            )
        )
    )

    fraud_df = (
        txn_features
        .join(
            card_features,
            "customer_id",
            "outer"
        )
        .join(
            device_features,
            "customer_id",
            "outer"
        )
        .fillna(0)
    )

    return fraud_df