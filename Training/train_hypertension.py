import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)


# --------------------------------------------------
# 1. Load Framingham dataset
# --------------------------------------------------

DATA_PATH = "datasets/framingham.csv"
MODEL_PATH = "models/hypertension_model.pkl"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)


# --------------------------------------------------
# 2. Select features and target
# --------------------------------------------------

features = [
    "male",
    "age",
    "glucose",
    "sysBP",
    "diaBP",
    "totChol",
    "heartRate"
]

target = "prevalentHyp"

X = df[features].copy()
y = df[target].copy()


# --------------------------------------------------
# 3. Convert values to numeric
# --------------------------------------------------

for column in features:
    X[column] = pd.to_numeric(X[column], errors="coerce")

y = pd.to_numeric(y, errors="coerce")


# Remove rows where target is missing
valid_rows = y.notna()

X = X.loc[valid_rows]
y = y.loc[valid_rows].astype(int)

print("Usable records:", len(X))

print("\nHypertension distribution:")
print(y.value_counts())


# --------------------------------------------------
# 4. Train/test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 5. Create ML pipeline
# --------------------------------------------------

model = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    ),
    (
        "scaler",
        StandardScaler()
    ),
    (
        "classifier",
        LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            random_state=42
        )
    )
])


# --------------------------------------------------
# 6. Train model
# --------------------------------------------------

model.fit(X_train, y_train)


# --------------------------------------------------
# 7. Make predictions
# --------------------------------------------------

y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)[:, 1]


# --------------------------------------------------
# 8. Evaluate model
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n==============================")
print("HYPERTENSION MODEL RESULTS")
print("==============================")

print(f"Accuracy : {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall   : {recall:.3f}")
print(f"F1 Score : {f1:.3f}")
print(f"ROC-AUC  : {roc_auc:.3f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["No Hypertension", "Hypertension"],
        zero_division=0
    )
)


# --------------------------------------------------
# 9. Save model
# --------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")
print(MODEL_PATH)