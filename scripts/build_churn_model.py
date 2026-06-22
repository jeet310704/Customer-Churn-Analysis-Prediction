"""
build_churn_model.py
Phase 4: Machine Learning - Churn Prediction

Trains a Logistic Regression and a Random Forest Classifier on the
cleaned customer churn dataset, evaluates both models, selects the
better one based on recall and F1-score, and saves:
  - Best model        -> models/churn_prediction_model.pkl
  - Feature columns   -> models/model_features.pkl
  - Evaluation report -> reports/model_evaluation_report.txt

Run from the project root:
    python scripts/build_churn_model.py
"""

import os
import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection    import train_test_split
from sklearn.linear_model       import LogisticRegression
from sklearn.ensemble           import RandomForestClassifier
from sklearn.preprocessing      import StandardScaler
from sklearn.pipeline           import Pipeline
from sklearn.metrics            import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)


# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

CLEAN_CSV     = os.path.join("data", "processed", "customer_churn_cleaned.csv")
MODEL_PATH    = os.path.join("models", "churn_prediction_model.pkl")
FEATURES_PATH = os.path.join("models", "model_features.pkl")
REPORT_PATH   = os.path.join("reports", "model_evaluation_report.txt")


# ------------------------------------------------------------------
# Helper: dual-output writer (terminal + saved report)
# ------------------------------------------------------------------

report_lines = []

def log(text=""):
    print(text)
    report_lines.append(str(text))

def section(title):
    border = "=" * 60
    log()
    log(border)
    log("  " + title)
    log(border)


# ------------------------------------------------------------------
# STEP 1 - Load the cleaned dataset
# ------------------------------------------------------------------

section("STEP 1 - LOAD DATA")

df = pd.read_csv(CLEAN_CSV)
log("Dataset loaded from: " + CLEAN_CSV)
log("Shape: " + str(df.shape))


# ------------------------------------------------------------------
# STEP 2 - Prepare features and target
# ------------------------------------------------------------------

section("STEP 2 - PREPARE FEATURES AND TARGET")

# Drop customer_id - it is just an identifier, not a useful feature
df = df.drop(columns=["customer_id"])

# Convert the target column: Yes -> 1, No -> 0
df["churn"] = df["churn"].map({"Yes": 1, "No": 0})

log("Target column (churn): Yes=1, No=0")
log("Churn value counts after encoding:")
log(df["churn"].value_counts().to_string())

# Separate features (X) and target (y)
X = df.drop(columns=["churn"])
y = df["churn"]

# Categorical columns that need one-hot encoding
cat_cols = ["gender", "contract_type", "payment_method", "internet_service"]

# Numeric columns - already in the right format
num_cols = ["age", "tenure", "monthly_charges", "total_charges", "support_calls"]

log("\nNumeric features  : " + str(num_cols))
log("Categorical features: " + str(cat_cols))

# One-hot encode the categorical columns
# drop_first=True removes one column per category to avoid multicollinearity
# (e.g. if gender has Male and Female, we only need one column)
X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

# Save the final list of feature column names.
# This is important: when we predict on new data later, it must have
# exactly the same columns in the same order.
feature_columns = list(X.columns)

log("\nTotal features after one-hot encoding: " + str(len(feature_columns)))
log("Feature columns:")
for col in feature_columns:
    log("  " + col)


# ------------------------------------------------------------------
# STEP 3 - Train/Test Split
# ------------------------------------------------------------------

section("STEP 3 - TRAIN / TEST SPLIT")

# stratify=y ensures both splits have the same ratio of churned/not-churned
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

log("Total samples  : " + str(len(X)))
log("Training set   : " + str(len(X_train)) + " rows (80%)")
log("Test set       : " + str(len(X_test))  + " rows (20%)")
log("Train churn rate: " + str(round(y_train.mean() * 100, 2)) + "%")
log("Test  churn rate: " + str(round(y_test.mean()  * 100, 2)) + "%")


# ------------------------------------------------------------------
# STEP 4 - Train Model 1: Logistic Regression
# ------------------------------------------------------------------

section("STEP 4 - MODEL 1: LOGISTIC REGRESSION")

# Logistic Regression works much better when numeric features are on
# the same scale. We use a Pipeline to chain StandardScaler (scales
# each feature to mean=0, std=1) directly into the model so both
# steps are bundled in one object and saved together.
lr_model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf",    LogisticRegression(random_state=42, max_iter=2000))
])
lr_model.fit(X_train, y_train)

lr_preds = lr_model.predict(X_test)

lr_accuracy  = round(accuracy_score(y_test,  lr_preds) * 100, 2)
lr_precision = round(precision_score(y_test, lr_preds) * 100, 2)
lr_recall    = round(recall_score(y_test,    lr_preds) * 100, 2)
lr_f1        = round(f1_score(y_test,        lr_preds) * 100, 2)
lr_cm        = confusion_matrix(y_test, lr_preds)

log("Logistic Regression Results:")
log("  Accuracy  : " + str(lr_accuracy)  + "%")
log("  Precision : " + str(lr_precision) + "%")
log("  Recall    : " + str(lr_recall)    + "%  <- how many churners we caught")
log("  F1-Score  : " + str(lr_f1)        + "%")
log("\nConfusion Matrix (Logistic Regression):")
log("  Predicted No  | Predicted Yes")
log("  Actual No  : " + str(lr_cm[0][0]) + "        | " + str(lr_cm[0][1]))
log("  Actual Yes : " + str(lr_cm[1][0]) + "        | " + str(lr_cm[1][1]))
log("\nClassification Report (Logistic Regression):")
log(classification_report(y_test, lr_preds, target_names=["No Churn", "Churn"]))


# ------------------------------------------------------------------
# STEP 5 - Train Model 2: Random Forest Classifier
# ------------------------------------------------------------------

section("STEP 5 - MODEL 2: RANDOM FOREST CLASSIFIER")

# Random Forest builds many decision trees and combines their votes.
# n_estimators=100 means 100 trees.
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

rf_preds = rf_model.predict(X_test)

rf_accuracy  = round(accuracy_score(y_test,  rf_preds) * 100, 2)
rf_precision = round(precision_score(y_test, rf_preds) * 100, 2)
rf_recall    = round(recall_score(y_test,    rf_preds) * 100, 2)
rf_f1        = round(f1_score(y_test,        rf_preds) * 100, 2)
rf_cm        = confusion_matrix(y_test, rf_preds)

log("Random Forest Results:")
log("  Accuracy  : " + str(rf_accuracy)  + "%")
log("  Precision : " + str(rf_precision) + "%")
log("  Recall    : " + str(rf_recall)    + "%  <- how many churners we caught")
log("  F1-Score  : " + str(rf_f1)        + "%")
log("\nConfusion Matrix (Random Forest):")
log("  Predicted No  | Predicted Yes")
log("  Actual No  : " + str(rf_cm[0][0]) + "        | " + str(rf_cm[0][1]))
log("  Actual Yes : " + str(rf_cm[1][0]) + "        | " + str(rf_cm[1][1]))
log("\nClassification Report (Random Forest):")
log(classification_report(y_test, rf_preds, target_names=["No Churn", "Churn"]))


# ------------------------------------------------------------------
# STEP 6 - Feature importances from Random Forest
# ------------------------------------------------------------------

section("STEP 6 - FEATURE IMPORTANCES (RANDOM FOREST)")

importances = pd.Series(rf_model.feature_importances_, index=feature_columns)
importances = importances.sort_values(ascending=False)

log("Top 10 features by importance:")
for feat, imp in importances.head(10).items():
    log("  " + feat.ljust(35) + str(round(imp * 100, 2)) + "%")


# ------------------------------------------------------------------
# STEP 7 - Compare models and select the best one
# ------------------------------------------------------------------

section("STEP 7 - MODEL COMPARISON AND SELECTION")

log("Metric comparison:")
log("  " + "Metric".ljust(14) + "Logistic Regression".ljust(24) + "Random Forest")
log("  " + "-" * 52)
log("  " + "Accuracy".ljust(14)  + str(lr_accuracy).ljust(24)  + str(rf_accuracy))
log("  " + "Precision".ljust(14) + str(lr_precision).ljust(24) + str(rf_precision))
log("  " + "Recall".ljust(14)    + str(lr_recall).ljust(24)    + str(rf_recall))
log("  " + "F1-Score".ljust(14)  + str(lr_f1).ljust(24)        + str(rf_f1))

# Selection logic: compare on recall first, then F1 as tiebreaker.
# In churn prediction, recall matters most - a missed churner costs
# more than a false alarm. A customer wrongly flagged just gets an
# extra retention offer; a missed churner walks away with no intervention.
log("\nSelection reasoning:")
log("  In churn prediction, Recall is the most important metric.")
log("  Missing a customer who will churn (false negative) is more costly")
log("  than a false alarm (false positive).")

if rf_recall > lr_recall:
    best_model   = rf_model
    best_name    = "Random Forest Classifier"
    best_recall  = rf_recall
    best_f1      = rf_f1
    other_recall = lr_recall
    other_f1     = lr_f1
    other_name   = "Logistic Regression"
elif lr_recall > rf_recall:
    best_model   = lr_model
    best_name    = "Logistic Regression"
    best_recall  = lr_recall
    best_f1      = lr_f1
    other_recall = rf_recall
    other_f1     = rf_f1
    other_name   = "Random Forest Classifier"
else:
    # Recalls are equal - use F1 as tiebreaker
    if rf_f1 >= lr_f1:
        best_model   = rf_model
        best_name    = "Random Forest Classifier"
        best_recall  = rf_recall
        best_f1      = rf_f1
        other_recall = lr_recall
        other_f1     = lr_f1
        other_name   = "Logistic Regression"
    else:
        best_model   = lr_model
        best_name    = "Logistic Regression"
        best_recall  = lr_recall
        best_f1      = lr_f1
        other_recall = rf_recall
        other_f1     = rf_f1
        other_name   = "Random Forest Classifier"

log("\nSELECTED MODEL: " + best_name)
log("  Recall  : " + str(best_recall) + "% (vs " + str(other_recall) + "% for " + other_name + ")")
log("  F1-Score: " + str(best_f1)     + "% (vs " + str(other_f1)     + "% for " + other_name + ")")


# ------------------------------------------------------------------
# STEP 8 - Save the best model and feature columns
# ------------------------------------------------------------------

section("STEP 8 - SAVE MODEL AND FEATURES")

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# Save the trained model using pickle
with open(MODEL_PATH, "wb") as f:
    pickle.dump(best_model, f)
log("Best model saved    -> " + MODEL_PATH)

# Save the feature column list so predictions on new data use the
# exact same columns in the exact same order
with open(FEATURES_PATH, "wb") as f:
    pickle.dump(feature_columns, f)
log("Feature columns saved -> " + FEATURES_PATH)
log("Feature count: " + str(len(feature_columns)))


# ------------------------------------------------------------------
# STEP 9 - Quick prediction demo (how to use the saved model)
# ------------------------------------------------------------------

section("STEP 9 - PREDICTION DEMO")

log("Loading saved model and making a test prediction...")

with open(MODEL_PATH, "rb") as f:
    loaded_model = pickle.load(f)

with open(FEATURES_PATH, "rb") as f:
    loaded_features = pickle.load(f)

# Create one example customer (high-risk profile)
sample = pd.DataFrame([{
    "age":             28,
    "tenure":           4,
    "monthly_charges": 95.0,
    "total_charges":  380.0,
    "support_calls":    7,
    "gender":        "Female",
    "contract_type": "Month-to-Month",
    "payment_method":"Electronic Check",
    "internet_service":"Fiber Optic"
}])

# Apply the same one-hot encoding as training
sample_encoded = pd.get_dummies(
    sample,
    columns=["gender", "contract_type", "payment_method", "internet_service"],
    drop_first=True
)

# Add any missing columns (set to 0) and reorder to match training
for col in loaded_features:
    if col not in sample_encoded.columns:
        sample_encoded[col] = 0
sample_encoded = sample_encoded[loaded_features]

prediction    = loaded_model.predict(sample_encoded)[0]
probability   = loaded_model.predict_proba(sample_encoded)[0]
churn_label   = "YES - Will Churn" if prediction == 1 else "NO - Will Not Churn"

log("Sample customer profile:")
log("  Age: 28 | Tenure: 4 months | Monthly Charges: $95 | Support Calls: 7")
log("  Contract: Month-to-Month | Payment: Electronic Check | Internet: Fiber Optic")
log("Prediction  : " + churn_label)
log("Probability : No Churn=" + str(round(probability[0]*100, 1)) + "% | Churn=" + str(round(probability[1]*100, 1)) + "%")


# ------------------------------------------------------------------
# STEP 10 - Save the evaluation report
# ------------------------------------------------------------------

section("SAVING REPORT")

os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("CUSTOMER CHURN ANALYSIS - MODEL EVALUATION REPORT\n")
    f.write("Phase 4: Machine Learning - Churn Prediction\n")
    f.write("=" * 60 + "\n\n")
    f.write("\n".join(report_lines))

log("Evaluation report saved -> " + REPORT_PATH)
log("\nPhase 4 complete.")
