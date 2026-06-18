import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier


print("\nLoading Prediction Dataset...")

df = pd.read_csv(
    "data/processed/prediction_dataset.csv"
)

# ---------------------------------
# Datetime Features
# ---------------------------------

df["created_datetime"] = pd.to_datetime(
    df["created_datetime"],
    errors="coerce"
)

df["hour"] = df["created_datetime"].dt.hour
df["month"] = df["created_datetime"].dt.month

df["is_weekend"] = (
    df["created_datetime"]
    .dt.dayofweek
    .isin([5, 6])
).astype(int)

# ---------------------------------
# Select Features
# ---------------------------------

features = [
    "hour",
    "month",
    "is_weekend",
    "vehicle_type",
    "violation_type",
    "police_station"
]

target = "high_risk_hotspot"

# ---------------------------------
# Remove Missing Values
# ---------------------------------

df = df[
    features + [target]
].dropna()

# ---------------------------------
# Label Encoding
# ---------------------------------

encoders = {}

categorical_cols = [
    "vehicle_type",
    "violation_type",
    "police_station"
]

for col in categorical_cols:

    le = LabelEncoder()

    df[col] = le.fit_transform(
        df[col].astype(str)
    )

    encoders[col] = le

# ---------------------------------
# X and Y
# ---------------------------------

X = df[features]

y = df[target]

# ---------------------------------
# Train Test Split
# ---------------------------------

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
)

# ---------------------------------
# Model
# ---------------------------------

print("\nTraining XGBoost...")

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss"
)

model.fit(
    X_train,
    y_train
)

# ---------------------------------
# Predictions
# ---------------------------------

preds = model.predict(
    X_test
)

# ---------------------------------
# Evaluation
# ---------------------------------

print("\nClassification Report")

print(
    classification_report(
        y_test,
        preds
    )
)

print("\nConfusion Matrix")

print(
    confusion_matrix(
        y_test,
        preds
    )
)

# ---------------------------------
# Feature Importance
# ---------------------------------

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance")

print(importance)

# ---------------------------------
# Save Model
# ---------------------------------

joblib.dump(
    model,
    "models/xgboost_model.pkl"
)

print(
    "\nSaved model -> models/xgboost_model.pkl"
)