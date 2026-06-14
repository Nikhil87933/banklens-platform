"""
schema_definitions.py
─────────────────────
Single source of truth for all BankLens table schemas.

This file drives:
  1. generate_column_mapping.py  →  produces column_mapping.csv (metadata)
  2. generate_data.py            →  date/timestamp formatting + column drift guard

Rules:
  - target_type must be one of: STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIMESTAMP
  - format_string is required for DATE (yyyy-MM-dd) and TIMESTAMP (yyyy-MM-dd HH:mm:ss)
  - format_string is empty string "" for all other types
  - Column order here must match the order rows are built in generate_data.py
  - is_active = True for all columns (kept for downstream Silver compatibility)

How to add a new column:
  1. Add the column dict to the correct table list below, in the correct position.
  2. Add the column to the corresponding gen_*() function in generate_data.py.
  3. Re-run generate_column_mapping.py to regenerate column_mapping.csv.
  If step 2 is missed, generate_data.py will raise a ColumnDriftError on next run.

How to add a new table:
  1. Add a new key to SCHEMA_REGISTRY with its column list.
  2. Add a new gen_*() function in generate_data.py.
  3. Re-run generate_column_mapping.py.
"""

# ── Type + format constants (avoids typos in the dicts below) ─────────────────
STRING    = "STRING"
INTEGER   = "INTEGER"
DECIMAL   = "DECIMAL"
BOOLEAN   = "BOOLEAN"
DATE      = "DATE"
TIMESTAMP = "TIMESTAMP"

DATE_FMT  = "yyyy-MM-dd"
TS_FMT    = "yyyy-MM-dd HH:mm:ss"
NO_FMT    = ""

# ── Schema registry ────────────────────────────────────────────────────────────
# Each entry: {"column_name": str, "target_type": str, "format_string": str, "is_active": bool}

SCHEMA_REGISTRY = {

    # ── 1. MERCHANT_REFERENCE ──────────────────────────────────────────────────
    "merchant_reference": [
        {"column_name": "merchant_id",       "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_name",     "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "mcc_code",          "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "mcc_description",   "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "category_group",    "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_city",     "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_state",    "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_country",  "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_lat",      "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_lon",      "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "is_high_risk_mcc",  "target_type": BOOLEAN, "format_string": NO_FMT,   "is_active": True},
    ],

    # ── 2. MARKET_RATES ────────────────────────────────────────────────────────
    "market_rates": [
        {"column_name": "rate_date",            "target_type": DATE,    "format_string": DATE_FMT, "is_active": True},
        {"column_name": "rate_type",            "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "rate_value",           "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "change_from_previous", "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "rba_decision",         "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
    ],

    # ── 3. CUSTOMER_MASTER ─────────────────────────────────────────────────────
    # FIX: relationship_manager_id is a UUID (STRING), not DECIMAL.
    #      The old extract_column_mapping.py inferred DECIMAL because row 0
    #      was a RETAIL customer (None → pandas NaN → isinstance float check hit).
    "customer_master": [
        {"column_name": "customer_id",             "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "customer_type",           "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "first_name",              "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "last_name",               "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "date_of_birth",           "target_type": DATE,      "format_string": DATE_FMT, "is_active": True},
        {"column_name": "gender",                  "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "state",                   "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "postcode",                "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "occupation_code",         "target_type": INTEGER,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "income_band",             "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "customer_since_date",     "target_type": DATE,      "format_string": DATE_FMT, "is_active": True},
        {"column_name": "kyc_status",              "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "preferred_channel",       "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "nps_score",               "target_type": INTEGER,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "segment_code",            "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "relationship_manager_id", "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},  # UUID or null — NOT DECIMAL
        {"column_name": "marketing_consent",       "target_type": BOOLEAN,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "created_at",              "target_type": TIMESTAMP, "format_string": TS_FMT,   "is_active": True},
        {"column_name": "updated_at",              "target_type": TIMESTAMP, "format_string": TS_FMT,   "is_active": True},
        # is_churn written by main() to preserve churn set across checkpoints — not a business column
        {"column_name": "is_churn",                "target_type": BOOLEAN,   "format_string": NO_FMT,   "is_active": True},
    ],

    # ── 4. ACCOUNT_MASTER ─────────────────────────────────────────────────────
    # FIX: close_date is a nullable DATE, not STRING.
    #      Old extractor saw None on row 0 (most accounts are open) → fell through to STRING.
    "account_master": [
        {"column_name": "account_id",            "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "customer_id",           "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "account_type",          "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "product_code",          "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "open_date",             "target_type": DATE,      "format_string": DATE_FMT, "is_active": True},
        {"column_name": "close_date",            "target_type": DATE,      "format_string": DATE_FMT, "is_active": True},  # nullable DATE — NOT STRING
        {"column_name": "account_status",        "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "currency_code",         "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "current_balance",       "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "available_balance",     "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "credit_limit",          "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "interest_rate",         "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "branch_code",           "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "is_primary_account",    "target_type": BOOLEAN,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "last_transaction_date", "target_type": DATE,      "format_string": DATE_FMT, "is_active": True},
        {"column_name": "overdraft_limit",       "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "created_at",            "target_type": TIMESTAMP, "format_string": TS_FMT,   "is_active": True},
        {"column_name": "updated_at",            "target_type": TIMESTAMP, "format_string": TS_FMT,   "is_active": True},
    ],

    # ── 5. LOAN_MASTER ────────────────────────────────────────────────────────
    # fixed_rate_expiry: nullable DATE — old extractor needed TYPE_OVERRIDES hack for this.
    # lvr: nullable DECIMAL — only set for HOME_LOAN, None otherwise.
    # property_state: nullable STRING — only set for HOME_LOAN.
    # offset_account_id: nullable STRING (UUID) — only set for HOME_LOAN.
    "loan_master": [
        {"column_name": "loan_id",              "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "account_id",           "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "customer_id",          "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "loan_type",            "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "loan_purpose",         "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "origination_date",     "target_type": DATE,    "format_string": DATE_FMT, "is_active": True},
        {"column_name": "maturity_date",        "target_type": DATE,    "format_string": DATE_FMT, "is_active": True},
        {"column_name": "original_principal",   "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "outstanding_balance",  "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "interest_rate_type",   "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "interest_rate",        "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "repayment_type",       "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "repayment_frequency",  "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "monthly_repayment",    "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "arrears_days",         "target_type": INTEGER, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "arrears_amount",       "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "lvr",                  "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},  # nullable — HOME_LOAN only
        {"column_name": "property_state",       "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},  # nullable — HOME_LOAN only
        {"column_name": "fixed_rate_expiry",    "target_type": DATE,    "format_string": DATE_FMT, "is_active": True},  # nullable — FIXED rate only; old extractor needed TYPE_OVERRIDES for this
        {"column_name": "offset_account_id",    "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},  # nullable UUID — HOME_LOAN only
    ],

    # ── 6. PRODUCT_HOLDINGS ───────────────────────────────────────────────────
    # FIX: end_date is a nullable DATE, not STRING.
    "product_holdings": [
        {"column_name": "holding_id",       "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "customer_id",      "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "product_category", "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "product_code",     "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "start_date",       "target_type": DATE,    "format_string": DATE_FMT, "is_active": True},
        {"column_name": "end_date",         "target_type": DATE,    "format_string": DATE_FMT, "is_active": True},  # nullable DATE — NOT STRING
        {"column_name": "status",           "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "is_primary",       "target_type": BOOLEAN, "format_string": NO_FMT,   "is_active": True},
    ],

    # ── 7. DEVICE_EVENTS ──────────────────────────────────────────────────────
    # session_duration_sec: nullable INTEGER — fraud rows (template 1/3) set it to None.
    # channel_action: nullable STRING — fraud device-register rows set it to None.
    "device_events": [
        {"column_name": "event_id",             "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "customer_id",          "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "device_id",            "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "event_timestamp",      "target_type": TIMESTAMP, "format_string": TS_FMT, "is_active": True},
        {"column_name": "event_type",           "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "device_type",          "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "device_model",         "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "os_version",           "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "app_version",          "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "ip_address",           "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "ip_country",           "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "ip_city",              "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "is_vpn",               "target_type": BOOLEAN,   "format_string": NO_FMT, "is_active": True},
        {"column_name": "is_jailbroken",        "target_type": BOOLEAN,   "format_string": NO_FMT, "is_active": True},
        {"column_name": "session_duration_sec", "target_type": INTEGER,   "format_string": NO_FMT, "is_active": True},  # nullable — fraud rows are None
        {"column_name": "login_success",        "target_type": BOOLEAN,   "format_string": NO_FMT, "is_active": True},
        {"column_name": "failed_auth_count",    "target_type": INTEGER,   "format_string": NO_FMT, "is_active": True},
        {"column_name": "channel_action",       "target_type": STRING,    "format_string": NO_FMT, "is_active": True},  # nullable — fraud device-register rows are None
    ],

    # ── 8. TRANSACTION_FACT ───────────────────────────────────────────────────
    "transaction_fact": [
        {"column_name": "transaction_id",        "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "account_id",            "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "customer_id",           "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "transaction_date",      "target_type": DATE,      "format_string": DATE_FMT, "is_active": True},
        {"column_name": "transaction_timestamp", "target_type": TIMESTAMP, "format_string": TS_FMT,   "is_active": True},
        {"column_name": "transaction_type",      "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "transaction_channel",   "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "amount",                "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "running_balance",       "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "counterparty_account",  "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "counterparty_bsb",      "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "counterparty_name",     "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "reference_text",        "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_id",           "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "mcc_code",              "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "country_code",          "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "city",                  "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "is_flagged",            "target_type": BOOLEAN,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "flag_reason",           "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "processing_date",       "target_type": DATE,      "format_string": DATE_FMT, "is_active": True},
        {"column_name": "batch_id",              "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
    ],

    # ── 9. CARD_TRANSACTION_FACT ──────────────────────────────────────────────
    # device_id: nullable STRING — only set for fraud templates 1 and 3.
    # ip_address: nullable STRING — only set for CNP transactions and fraud rows.
    # dispute_reason: nullable STRING — only set when is_disputed = True.
    "card_transaction_fact": [
        {"column_name": "card_txn_id",      "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "card_id",          "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "account_id",       "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "customer_id",      "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "auth_timestamp",   "target_type": TIMESTAMP, "format_string": TS_FMT,   "is_active": True},
        {"column_name": "settlement_date",  "target_type": DATE,      "format_string": DATE_FMT, "is_active": True},
        {"column_name": "amount",           "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "currency_code",    "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "aud_amount",       "target_type": DECIMAL,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_id",      "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_name",    "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "mcc_code",         "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_country", "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "merchant_city",    "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "terminal_type",    "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "entry_mode",       "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "is_cnp",           "target_type": BOOLEAN,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "is_international", "target_type": BOOLEAN,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "device_id",        "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},  # nullable — fraud only
        {"column_name": "ip_address",       "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},  # nullable — CNP + fraud only
        {"column_name": "response_code",    "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "is_disputed",      "target_type": BOOLEAN,   "format_string": NO_FMT,   "is_active": True},
        {"column_name": "dispute_reason",   "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},  # nullable
        {"column_name": "auth_code",        "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
        {"column_name": "batch_id",         "target_type": STRING,    "format_string": NO_FMT,   "is_active": True},
    ],

    # ── 10. ACCOUNT_BALANCE_SNAPSHOT ──────────────────────────────────────────
    "account_balance_snapshot": [
        {"column_name": "snapshot_id",     "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "account_id",      "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "customer_id",     "target_type": STRING,  "format_string": NO_FMT,   "is_active": True},
        {"column_name": "snapshot_date",   "target_type": DATE,    "format_string": DATE_FMT, "is_active": True},
        {"column_name": "closing_balance", "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "average_balance", "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "min_balance",     "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "max_balance",     "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "credit_count",    "target_type": INTEGER, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "debit_count",     "target_type": INTEGER, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "total_credits",   "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "total_debits",    "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
        {"column_name": "fee_amount",      "target_type": DECIMAL, "format_string": NO_FMT,   "is_active": True},
    ],

    # ── 11. DIGITAL_ACTIVITY ──────────────────────────────────────────────────
    "digital_activity": [
        {"column_name": "activity_id",        "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "customer_id",        "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "session_id",         "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "activity_timestamp", "target_type": TIMESTAMP, "format_string": TS_FMT, "is_active": True},
        {"column_name": "activity_type",      "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "channel",            "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "feature_area",       "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "duration_seconds",   "target_type": INTEGER,   "format_string": NO_FMT, "is_active": True},
        {"column_name": "is_completed",       "target_type": BOOLEAN,   "format_string": NO_FMT, "is_active": True},
    ],

    # ── 12. SUPPORT_TICKETS ───────────────────────────────────────────────────
    # FIX: resolved_at is a nullable TIMESTAMP, not STRING.
    # FIX: resolution_hours is a nullable INTEGER, not STRING.
    #      Both were inferred as STRING because row 0 was often an unresolved ticket (None).
    "support_tickets": [
        {"column_name": "ticket_id",           "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "customer_id",         "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "account_id",          "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "created_at",          "target_type": TIMESTAMP, "format_string": TS_FMT, "is_active": True},
        {"column_name": "resolved_at",         "target_type": TIMESTAMP, "format_string": TS_FMT, "is_active": True},  # nullable — NOT STRING
        {"column_name": "resolution_hours",    "target_type": INTEGER,   "format_string": NO_FMT, "is_active": True},  # nullable — NOT STRING
        {"column_name": "channel",             "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "ticket_category",     "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "ticket_subcategory",  "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "priority",            "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "status",              "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "sentiment_score",     "target_type": DECIMAL,   "format_string": NO_FMT, "is_active": True},
        {"column_name": "subject",             "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "description",         "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "resolution_notes",    "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
        {"column_name": "escalated_flag",      "target_type": BOOLEAN,   "format_string": NO_FMT, "is_active": True},
        {"column_name": "nps_post_resolution", "target_type": INTEGER,   "format_string": NO_FMT, "is_active": True},
        {"column_name": "agent_id",            "target_type": STRING,    "format_string": NO_FMT, "is_active": True},
    ],
}


# ── Convenience lookups (used by generate_data.py) ────────────────────────────

def get_columns(table_name: str) -> list[str]:
    """Return ordered list of column names for a table."""
    return [col["column_name"] for col in SCHEMA_REGISTRY[table_name]]


def get_date_columns(table_name: str) -> list[str]:
    """Return column names where target_type is DATE."""
    return [
        col["column_name"]
        for col in SCHEMA_REGISTRY[table_name]
        if col["target_type"] == DATE
    ]


def get_timestamp_columns(table_name: str) -> list[str]:
    """Return column names where target_type is TIMESTAMP."""
    return [
        col["column_name"]
        for col in SCHEMA_REGISTRY[table_name]
        if col["target_type"] == TIMESTAMP
    ]


def get_format(table_name: str, column_name: str) -> str:
    """Return format_string for a specific column."""
    for col in SCHEMA_REGISTRY[table_name]:
        if col["column_name"] == column_name:
            return col["format_string"]
    raise KeyError(f"Column '{column_name}' not found in table '{table_name}'")


# ── Self-validation (runs on import) ──────────────────────────────────────────

def _validate_registry():
    """
    Sanity-check the registry on import.
    Catches: unsupported types, DATE/TIMESTAMP without format, non-DATE/TIMESTAMP with format.
    """
    valid_types = {STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIMESTAMP}
    errors = []

    for table, cols in SCHEMA_REGISTRY.items():
        seen = set()
        for col in cols:
            name   = col["column_name"]
            ttype  = col["target_type"]
            fmt    = col["format_string"]

            if name in seen:
                errors.append(f"{table}.{name}: duplicate column name")
            seen.add(name)

            if ttype not in valid_types:
                errors.append(f"{table}.{name}: unknown type '{ttype}'")

            if ttype in (DATE, TIMESTAMP) and not fmt:
                errors.append(f"{table}.{name}: type {ttype} must have a format_string")

            if ttype not in (DATE, TIMESTAMP) and fmt:
                errors.append(f"{table}.{name}: type {ttype} should not have a format_string")

    if errors:
        raise ValueError(
            "schema_definitions.py validation failed:\n" +
            "\n".join(f"  • {e}" for e in errors)
        )


_validate_registry()
