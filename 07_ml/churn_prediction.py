from pyspark.sql import functions as F
import pandas as pd

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
# Metrics
# --------------------------------------------------

print("Accuracy :", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions))
print("Recall   :", recall_score(y_test, predictions))
print("F1 Score :", f1_score(y_test, predictions))
print("ROC AUC  :", roc_auc_score(y_test, probabilities))