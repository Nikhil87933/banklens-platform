from pyspark.sql import functions as F
import pandas as pd
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

# --------------------------------------------------
# Load Gold Churn Features
# --------------------------------------------------

df = spark.table(
    "banklens.gold.gld_churn_features"
)

pdf = df.toPandas()

# --------------------------------------------------
# Encode Customer Type
# --------------------------------------------------

encoder = LabelEncoder()

pdf["customer_type"] = encoder.fit_transform(
    pdf["customer_type"]
)

# --------------------------------------------------
# Features and Target
# --------------------------------------------------

X = pdf[
    [
        "customer_type",
        "nps_score",
        "digital_sessions",
        "support_ticket_count",
        "product_count",
        "total_accounts",
        "total_balance",
        "tenure_days",
    ]
]

y = pdf["is_churn"]

# --------------------------------------------------
# Train Test Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# --------------------------------------------------
# Model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
)

model.fit(X_train, y_train)

# --------------------------------------------------
# Predictions
# --------------------------------------------------

predictions = model.predict(X_test)

probabilities = model.predict_proba(X_test)[:, 1]

# --------------------------------------------------
# Score Entire Dataset
# --------------------------------------------------

full_probabilities = model.predict_proba(X)[:, 1]

pdf["churn_probability"] = full_probabilities

pdf["churn_prediction"] = (
    pdf["churn_probability"] >= 0.50
)

pdf["risk_band"] = "LOW"

pdf.loc[
    pdf["churn_probability"] >= 0.70,
    "risk_band"
] = "HIGH"

pdf.loc[
    (
        pdf["churn_probability"] >= 0.40
    )
    &
    (
        pdf["churn_probability"] < 0.70
    ),
    "risk_band"
] = "MEDIUM"

pdf["prediction_timestamp"] = datetime.now()

# --------------------------------------------------
# Create Prediction Table
# --------------------------------------------------

prediction_df = pdf[
    [
        "customer_id",
        "churn_probability",
        "churn_prediction",
        "risk_band",
        "prediction_timestamp",
    ]
]

spark_prediction_df = spark.createDataFrame(
    prediction_df
)

spark.sql(
    """
    CREATE SCHEMA IF NOT EXISTS banklens.ml
    """
)

spark_prediction_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable(
        "banklens.ml.churn_predictions"
    )

print(
    "Churn Predictions Created"
)

print(
    "Rows =",
    spark_prediction_df.count()
)

# --------------------------------------------------
# Metrics
# --------------------------------------------------

print("Accuracy :", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions))
print("Recall   :", recall_score(y_test, predictions))
print("F1 Score :", f1_score(y_test, predictions))
print("ROC AUC  :", roc_auc_score(y_test, probabilities))