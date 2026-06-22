"""
clean_and_explore_churn_data.py
Phase 2: Data Cleaning & Exploration

Loads the raw customer churn dataset, performs quality checks,
cleans and validates the data, explores churn patterns, then saves:
  - Cleaned dataset -> data/processed/customer_churn_cleaned.csv
  - EDA summary     -> reports/churn_eda_summary.txt

Run from the project root:
    python scripts/clean_and_explore_churn_data.py
"""

import os
import pandas as pd
import numpy as np


# ----------------------------------------------------------------------
# HELPER: dual-output writer
# Prints every line to the terminal AND collects it for the .txt report.
# ----------------------------------------------------------------------

report_lines = []

def log(text=""):
    """Print to console and store for the summary report."""
    print(text)
    report_lines.append(str(text))

def section(title):
    """Print a clearly visible section header."""
    border = "=" * 60
    log()
    log(border)
    log("  " + title)
    log(border)


# ----------------------------------------------------------------------
# STEP 1 - Load the raw dataset
# ----------------------------------------------------------------------

RAW_PATH    = os.path.join("data", "raw",       "customer_churn_raw.csv")
CLEAN_PATH  = os.path.join("data", "processed", "customer_churn_cleaned.csv")
REPORT_PATH = os.path.join("reports",            "churn_eda_summary.txt")

log("Loading raw dataset...")
df = pd.read_csv(RAW_PATH)
log("Raw file loaded from: " + RAW_PATH)


# ----------------------------------------------------------------------
# STEP 2 - Basic data quality checks (on original column names)
# ----------------------------------------------------------------------

section("DATA QUALITY CHECKS")

# Shape
log("Shape (rows, columns): " + str(df.shape))

# Column names
log("\nColumn names:")
for col in df.columns:
    log("  " + col)

# Data types
log("\nData types:")
log(df.dtypes.to_string())

# Missing values
log("\nMissing values per column:")
missing = df.isnull().sum()
log(missing.to_string())
total_missing = missing.sum()
log("\nTotal missing values: " + str(total_missing))

# Duplicate rows
duplicate_count = df.duplicated().sum()
log("Duplicate rows found: " + str(duplicate_count))

# Unique values for categorical columns
log("\nUnique values - categorical columns:")
cat_cols = ["Gender", "Contract Type", "Payment Method", "Internet Service", "Churn"]
for col in cat_cols:
    log("  " + col + ": " + str(sorted(df[col].unique().tolist())))

# Basic statistics for numeric columns
log("\nBasic statistics - numeric columns:")
log(df.describe().round(2).to_string())


# ----------------------------------------------------------------------
# STEP 3 - Clean the dataset
# ----------------------------------------------------------------------

section("DATA CLEANING")

# 3a. Remove duplicate rows
before = len(df)
df = df.drop_duplicates()
after = len(df)
removed = before - after
log("Duplicate rows removed: " + str(removed))
log("Rows remaining after deduplication: " + str(after))

# 3b. Standardize column names to snake_case
column_rename_map = {
    "Customer ID":     "customer_id",
    "Gender":          "gender",
    "Age":             "age",
    "Tenure":          "tenure",
    "Contract Type":   "contract_type",
    "Payment Method":  "payment_method",
    "Monthly Charges": "monthly_charges",
    "Total Charges":   "total_charges",
    "Support Calls":   "support_calls",
    "Internet Service":"internet_service",
    "Churn":           "churn",
}

df = df.rename(columns=column_rename_map)

log("\nColumns renamed to snake_case:")
for old, new in column_rename_map.items():
    log("  '" + old + "'  ->  '" + new + "'")

log("\nNew column names confirmed:")
log(str(list(df.columns)))


# ----------------------------------------------------------------------
# STEP 4 - Validate the data
# ----------------------------------------------------------------------

section("DATA VALIDATION")

issues_found = 0

# Age must be between 1 and 120
invalid_age = df[(df["age"] < 1) | (df["age"] > 120)]
log("Invalid age values (outside 1-120): " + str(len(invalid_age)))
if len(invalid_age) > 0:
    log(invalid_age[["customer_id", "age"]].to_string(index=False))
    issues_found += len(invalid_age)

# Tenure must be at least 1 month
invalid_tenure = df[df["tenure"] < 1]
log("Invalid tenure values (< 1 month): " + str(len(invalid_tenure)))
if len(invalid_tenure) > 0:
    log(invalid_tenure[["customer_id", "tenure"]].to_string(index=False))
    issues_found += len(invalid_tenure)

# Monthly charges must be positive
invalid_monthly = df[df["monthly_charges"] <= 0]
log("Invalid monthly_charges (<= 0): " + str(len(invalid_monthly)))
if len(invalid_monthly) > 0:
    log(invalid_monthly[["customer_id", "monthly_charges"]].to_string(index=False))
    issues_found += len(invalid_monthly)

# Total charges must be positive
invalid_total = df[df["total_charges"] <= 0]
log("Invalid total_charges (<= 0): " + str(len(invalid_total)))
if len(invalid_total) > 0:
    log(invalid_total[["customer_id", "total_charges"]].to_string(index=False))
    issues_found += len(invalid_total)

# Support calls must not be negative
invalid_calls = df[df["support_calls"] < 0]
log("Invalid support_calls (< 0): " + str(len(invalid_calls)))
if len(invalid_calls) > 0:
    log(invalid_calls[["customer_id", "support_calls"]].to_string(index=False))
    issues_found += len(invalid_calls)

# Churn must only be Yes or No
invalid_churn = df[~df["churn"].isin(["Yes", "No"])]
log("Invalid churn values (not Yes/No): " + str(len(invalid_churn)))
if len(invalid_churn) > 0:
    log(invalid_churn[["customer_id", "churn"]].to_string(index=False))
    issues_found += len(invalid_churn)

if issues_found == 0:
    log("\nValidation result: PASSED - no data issues found.")
else:
    log("\nValidation result: " + str(issues_found) + " issue(s) found. Review above.")


# ----------------------------------------------------------------------
# STEP 5 - Churn exploration
# ----------------------------------------------------------------------

section("CHURN EXPLORATION")

total_customers = len(df)

# 5a. Overall churn count and percentage
log("--- Overall Churn ---")
churn_counts = df["churn"].value_counts()
churn_pct    = df["churn"].value_counts(normalize=True).mul(100).round(2)
churn_summary = pd.DataFrame({"Count": churn_counts, "Percentage (%)": churn_pct})
log(churn_summary.to_string())

# 5b. Churn by gender
log("\n--- Churn by Gender ---")
by_gender = (
    df.groupby("gender")["churn"]
    .value_counts(normalize=True)
    .mul(100).round(2)
    .rename("Churn %")
    .reset_index()
)
log(by_gender.to_string(index=False))

# 5c. Churn by contract type
log("\n--- Churn by Contract Type ---")
by_contract = (
    df.groupby("contract_type")["churn"]
    .value_counts(normalize=True)
    .mul(100).round(2)
    .rename("Churn %")
    .reset_index()
)
log(by_contract.to_string(index=False))

# 5d. Churn by payment method
log("\n--- Churn by Payment Method ---")
by_payment = (
    df.groupby("payment_method")["churn"]
    .value_counts(normalize=True)
    .mul(100).round(2)
    .rename("Churn %")
    .reset_index()
)
log(by_payment.to_string(index=False))

# 5e. Churn by internet service
log("\n--- Churn by Internet Service ---")
by_internet = (
    df.groupby("internet_service")["churn"]
    .value_counts(normalize=True)
    .mul(100).round(2)
    .rename("Churn %")
    .reset_index()
)
log(by_internet.to_string(index=False))

# 5f. Average monthly charges by churn
log("\n--- Average Monthly Charges by Churn ---")
avg_monthly = (
    df.groupby("churn")["monthly_charges"]
    .mean().round(2)
    .rename("Avg Monthly Charges ($)")
)
log(avg_monthly.to_string())

# 5g. Average tenure by churn
log("\n--- Average Tenure by Churn ---")
avg_tenure = (
    df.groupby("churn")["tenure"]
    .mean().round(2)
    .rename("Avg Tenure (months)")
)
log(avg_tenure.to_string())

# 5h. Average support calls by churn
log("\n--- Average Support Calls by Churn ---")
avg_calls = (
    df.groupby("churn")["support_calls"]
    .mean().round(2)
    .rename("Avg Support Calls")
)
log(avg_calls.to_string())


# ----------------------------------------------------------------------
# STEP 6 - Key insights summary
# ----------------------------------------------------------------------

section("KEY INSIGHTS")

churned     = df[df["churn"] == "Yes"]
not_churned = df[df["churn"] == "No"]

churn_rate = round(len(churned) / total_customers * 100, 2)

log("Total customers         : " + str(total_customers))
log("Churned customers       : " + str(len(churned)) + " (" + str(churn_rate) + "%)")
log("Retained customers      : " + str(len(not_churned)) + " (" + str(round(100 - churn_rate, 2)) + "%)")

log("\nAvg monthly charge - churned   : $" + str(round(churned["monthly_charges"].mean(), 2)))
log("Avg monthly charge - retained  : $" + str(round(not_churned["monthly_charges"].mean(), 2)))

log("\nAvg tenure - churned           : " + str(round(churned["tenure"].mean(), 1)) + " months")
log("Avg tenure - retained          : " + str(round(not_churned["tenure"].mean(), 1)) + " months")

log("\nAvg support calls - churned    : " + str(round(churned["support_calls"].mean(), 2)))
log("Avg support calls - retained   : " + str(round(not_churned["support_calls"].mean(), 2)))

top_contract = df[df["churn"] == "Yes"]["contract_type"].value_counts().idxmax()
log("\nMost common contract for churned customers  : " + top_contract)

top_payment = df[df["churn"] == "Yes"]["payment_method"].value_counts().idxmax()
log("Most common payment method for churned customers : " + top_payment)


# ----------------------------------------------------------------------
# STEP 7 - Save outputs
# ----------------------------------------------------------------------

section("SAVING OUTPUTS")

# Save cleaned CSV (never overwrites raw)
os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
df.to_csv(CLEAN_PATH, index=False)
log("Cleaned dataset saved  -> " + CLEAN_PATH)
log("  Rows    : " + str(len(df)))
log("  Columns : " + str(len(df.columns)))
log("  Columns : " + str(list(df.columns)))

# Save EDA summary text report
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("CUSTOMER CHURN ANALYSIS - EDA SUMMARY REPORT\n")
    f.write("Phase 2: Data Cleaning & Exploration\n")
    f.write("=" * 60 + "\n\n")
    f.write("\n".join(report_lines))
log("EDA summary saved      -> " + REPORT_PATH)

# Confirm raw file is untouched
raw_rows = len(pd.read_csv(RAW_PATH))
log("\nRaw dataset check: " + RAW_PATH + " still has " + str(raw_rows) + " rows - untouched.")

log("\nPhase 2 complete.")
