from customer_360 import build_customer_360

gold_df = build_customer_360(spark)

(
    gold_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(
        "banklens.gold.gold_customer_360"
    )
)

print("Customer 360 Gold created")
print("Rows =", gold_df.count())