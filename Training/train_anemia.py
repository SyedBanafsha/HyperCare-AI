import os
import pandas as pd

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

import joblib


# --------------------------------------------------
# 1. Load CKD dataset
# --------------------------------------------------

DATA_PATH = "datasets/chronic_kidney_disease.csv"
MODEL_PATH = "models/anemia_model.pkl"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)


# --------------------------------------------------
# 2. Select features and target
# --------------------------------------------------

# These are the measurements our HyperCare AI
# interface can provide for anemia screening.
features = [
    "age",
    "bp",
    "bgr",
    "hemo"
]

target = "ane"


X = df[features].copy()
y = df[target].copy()


# --------------------------------------------------
# 3. Clean missing values
# --------------------------------------------------

# The CKD dataset uses '?' for missing values.
X = X.replace("?", pd.NA)

# Convert all feature columns to numbers.
for column in features:
    X[column] = pd.to_numeric(X[column], errors="coerce")


# Clean target
y = y.replace("?", pd.NA)
y = y.astype("string").str.strip().str.lower()

# Convert:
# no  -> 0
# yes -> 1
y = y.map({
    "no": 0,
    "yes": 1
})


# Remove rows where the target is missing
valid_rows = y.notna()

X = X.loc[valid_rows]
y = y.loc[valid_rows].astype(int)


print("Usable records:", len(X))
print("Anemia distribution:")
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
# 5. Build ML pipeline
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
# 7. Evaluate model
# --------------------------------------------------

y_pred = model.predict(X_test)
y_probability = model.predict_proba(X_test)[:, 1]


accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_probability)


print("\n==============================")
print("ANEMIA MODEL RESULTS")
print("==============================")

print(f"Accuracy : {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall   : {recall:.3f}")
print(f"F1 Score : {f1:.3f}")
print(f"ROC-AUC  : {roc_auc:.3f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["No Anemia", "Anemia"],
    zero_division=0
))


# --------------------------------------------------
# 8. Save trained model
# --------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")
print(MODEL_PATH)