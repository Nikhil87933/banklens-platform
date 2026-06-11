import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, date


sys.path.insert(
    0,
    "/home/nikhil/banking_datagen"
)

import generate_data as gen


def infer_type(value):

    if isinstance(value, (bool, np.bool_)):
        return "BOOLEAN", ""

    if isinstance(value, (pd.Timestamp, datetime)):
        return "TIMESTAMP", "yyyy-MM-dd HH:mm:ss"

    if isinstance(value, date):
        return "DATE", "yyyy-MM-dd"

    if isinstance(value, (float, np.floating)):
        return "DECIMAL", ""

    if isinstance(value, (int, np.integer)):
        return "INTEGER", ""

    return "STRING", ""

TYPE_OVERRIDES = {
    ("loan_master", "fixed_rate_expiry"): (
        "DATE",
        "yyyy-MM-dd"
    )
}

def extract_df(table_name, df):

    if len(df) == 0:
        print(f"Skipping empty table: {table_name}")
        return []

    sample = df.iloc[0]

    rows = []

    for column_name in df.columns:

        value = sample[column_name]

        target_type, format_string = infer_type(value)

        target_type, format_string = infer_type(value)

        override = TYPE_OVERRIDES.get(
            (table_name, column_name)
        )

        if override:
            target_type, format_string = override

        rows.append(
            {
                "table_name": table_name,
                "column_name": column_name,
                "target_type": target_type,
                "format_string": format_string,
                "is_active": True
            }
        )

    return rows


all_rows = []

print("Generating metadata...")


customers_df, churn_ids = gen.gen_customers(n=500)

accounts_df, _ = gen.gen_accounts(
    customers_df
)

merchants_df = gen.gen_merchant_reference(
    n=10
)

fraud_customers = {}

cust_state_lookup = (
    customers_df
    .set_index("customer_id")["state"]
    .to_dict()
)

tables = {

    "merchant_reference":
        merchants_df,

    "market_rates":
        gen.gen_market_rates(),

    "customer_master":
        customers_df,

    "account_master":
        accounts_df,

    "loan_master":
        gen.gen_loans(
            accounts_df,
            churn_ids
        ),

    "product_holdings":
        gen.gen_product_holdings(
            accounts_df,
            churn_ids
        ),

    "device_events":
        gen.gen_device_events(
            customers_df,
            1,
            churn_ids
        )[0],
    "transaction_fact":
    gen.gen_transactions(
        customers_df,
        accounts_df,
        merchants_df,
        1,
        churn_ids,
        fraud_customers
    ),

    "card_transaction_fact":
        gen.gen_card_transactions(
            customers_df,
            accounts_df,
            merchants_df,
            1,
            churn_ids,
            fraud_customers,
            cust_state_lookup
        ),

    "digital_activity":
        gen.gen_digital_activity(
            customers_df,
            1,
            churn_ids
        ),

    "account_balance_snapshot":
        gen.gen_balance_snapshot(
            accounts_df,
            1,
            churn_ids
        ),

    "support_tickets":
        gen.gen_support_tickets(
            customers_df,
            accounts_df,
            1,
            churn_ids
        )
}

for table_name, df in tables.items():

    print(f"Processing {table_name}")
    print(f"Rows = {len(df)}")

    if table_name == "device_events":

        print(df.dtypes)

        print(df.head())

    all_rows.extend(
        extract_df(
            table_name,
            df
        )
    )


metadata_df = pd.DataFrame(
    all_rows
)

output_file = (
    Path(__file__).parent
    / "column_mapping.csv"
)

metadata_df.to_csv(
    output_file,
    index=False
)

print(
    f"\nGenerated {len(metadata_df)} metadata rows"
)

print(
    f"Written to {output_file}"
)