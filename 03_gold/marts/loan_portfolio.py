from pyspark.sql import functions as F


def build_loan_portfolio(spark):

    loan_df = spark.table(
        "banklens.silver.slv_loan_master"
    )

    gold_df = (
        loan_df
        .groupBy(
            "loan_type",
            "property_state"
        )
        .agg(
            F.count(
                "loan_id"
            ).alias(
                "loan_count"
            ),

            F.countDistinct(
                "customer_id"
            ).alias(
                "customer_count"
            ),

            F.sum(
                "original_principal"
            ).alias(
                "total_original_principal"
            ),

            F.sum(
                "outstanding_balance"
            ).alias(
                "total_outstanding_balance"
            ),

            F.avg(
                "interest_rate"
            ).alias(
                "avg_interest_rate"
            ),

            F.sum(
                F.when(
                    F.col(
                        "arrears_days"
                    ) > 0,
                    1
                ).otherwise(
                    0
                )
            ).alias(
                "arrears_customer_count"
            ),

            F.sum(
                "arrears_amount"
            ).alias(
                "total_arrears_amount"
            ),

            F.avg(
                "lvr"
            ).alias(
                "avg_lvr"
            )
        )
    )

    return gold_df