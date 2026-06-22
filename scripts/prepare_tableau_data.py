"""
prepare_tableau_data.py
Phase 5: Tableau Dashboard Preparation

Loads the cleaned dataset, adds dashboard-friendly columns, and saves
a Tableau-ready CSV to tableau/customer_churn_tableau.csv.

New columns added:
  churn_numeric        - 1 = churned, 0 = retained
  age_group            - age buckets for grouping charts
  tenure_group         - tenure buckets for grouping charts
  monthly_charge_group - Low / Medium / High charge tiers
  support_call_group   - call volume buckets
  customer_risk_level  - High / Medium / Low based on churn risk factors

Run from the project root:
    python scripts/prepare_tableau_data.py
"""

import os
import pandas as pd


# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

CLEAN_CSV   = os.path.join("data",    "processed", "customer_churn_cleaned.csv")
TABLEAU_CSV = os.path.join("tableau", "customer_churn_tableau.csv")


# ------------------------------------------------------------------
# STEP 1 - Load the cleaned dataset
# ------------------------------------------------------------------

print("Loading cleaned dataset...")
df = pd.read_csv(CLEAN_CSV)
print("  Rows    : " + str(len(df)))
print("  Columns : " + str(len(df.columns)))


# ------------------------------------------------------------------
# STEP 2 - churn_numeric
# Convert Yes/No text to 1/0 so Tableau can SUM and AVG it directly.
# ------------------------------------------------------------------

df["churn_numeric"] = df["churn"].map({"Yes": 1, "No": 0})
print("\nAdded: churn_numeric (Yes=1, No=0)")


# ------------------------------------------------------------------
# STEP 3 - age_group
# Bucket ages into readable ranges for bar/pie charts.
# ------------------------------------------------------------------

def get_age_group(age):
    if age <= 25:
        return "18-25"
    elif age <= 35:
        return "26-35"
    elif age <= 45:
        return "36-45"
    elif age <= 55:
        return "46-55"
    else:
        return "56+"

df["age_group"] = df["age"].apply(get_age_group)
print("Added: age_group (18-25 / 26-35 / 36-45 / 46-55 / 56+)")
print("  Distribution:")
for grp, cnt in df["age_group"].value_counts().sort_index().items():
    print("    " + grp + ": " + str(cnt))


# ------------------------------------------------------------------
# STEP 4 - tenure_group
# Bucket tenure into readable ranges.
# Thresholds reflect natural customer lifecycle stages.
# ------------------------------------------------------------------

def get_tenure_group(tenure):
    if tenure <= 12:
        return "0-12 Months"
    elif tenure <= 24:
        return "13-24 Months"
    elif tenure <= 48:
        return "25-48 Months"
    else:
        return "49+ Months"

df["tenure_group"] = df["tenure"].apply(get_tenure_group)
print("\nAdded: tenure_group (0-12 / 13-24 / 25-48 / 49+ Months)")
print("  Distribution:")
for grp, cnt in df["tenure_group"].value_counts().items():
    print("    " + grp + ": " + str(cnt))


# ------------------------------------------------------------------
# STEP 5 - monthly_charge_group
# Thresholds based on dataset quartiles:
#   Low    : < $45  (below 25th percentile)
#   Medium : $45-$80
#   High   : > $80  (above approx 75th percentile)
# ------------------------------------------------------------------

def get_charge_group(charge):
    if charge < 45:
        return "Low"
    elif charge <= 80:
        return "Medium"
    else:
        return "High"

df["monthly_charge_group"] = df["monthly_charges"].apply(get_charge_group)
print("\nAdded: monthly_charge_group (Low <$45 / Medium $45-80 / High >$80)")
print("  Distribution:")
for grp, cnt in df["monthly_charge_group"].value_counts().items():
    print("    " + grp + ": " + str(cnt))


# ------------------------------------------------------------------
# STEP 6 - support_call_group
# Groups support call volume into three tiers.
# ------------------------------------------------------------------

def get_call_group(calls):
    if calls <= 1:
        return "0-1 Calls"
    elif calls <= 3:
        return "2-3 Calls"
    else:
        return "4+ Calls"

df["support_call_group"] = df["support_calls"].apply(get_call_group)
print("\nAdded: support_call_group (0-1 / 2-3 / 4+ Calls)")
print("  Distribution:")
for grp, cnt in df["support_call_group"].value_counts().items():
    print("    " + grp + ": " + str(cnt))


# ------------------------------------------------------------------
# STEP 7 - customer_risk_level
# Count how many of the 5 known churn risk factors apply to each
# customer, then assign a tier:
#   3+ factors -> High Risk
#   1-2 factors -> Medium Risk
#   0 factors  -> Low Risk
#
# Risk factors:
#   1. Month-to-Month contract
#   2. Electronic Check payment
#   3. Monthly charges above $70
#   4. 4 or more support calls
#   5. Tenure of 12 months or fewer
# ------------------------------------------------------------------

def get_risk_level(row):
    score = 0
    if row["contract_type"]  == "Month-to-Month":  score += 1
    if row["payment_method"] == "Electronic Check": score += 1
    if row["monthly_charges"] > 70:                 score += 1
    if row["support_calls"]  >= 4:                  score += 1
    if row["tenure"]         <= 12:                 score += 1

    if score >= 3:
        return "High Risk"
    elif score >= 1:
        return "Medium Risk"
    else:
        return "Low Risk"

df["customer_risk_level"] = df.apply(get_risk_level, axis=1)
print("\nAdded: customer_risk_level (High / Medium / Low Risk)")
print("  Risk factor scoring:")
print("    +1 Month-to-Month contract")
print("    +1 Electronic Check payment")
print("    +1 Monthly charges > $70")
print("    +1 Support calls >= 4")
print("    +1 Tenure <= 12 months")
print("    3+ = High Risk  |  1-2 = Medium Risk  |  0 = Low Risk")
print("  Distribution:")
for grp, cnt in df["customer_risk_level"].value_counts().items():
    print("    " + grp + ": " + str(cnt))


# ------------------------------------------------------------------
# STEP 8 - Verify the new columns
# ------------------------------------------------------------------

print("\nFinal column list (" + str(len(df.columns)) + " columns):")
for col in df.columns:
    print("  " + col)


# ------------------------------------------------------------------
# STEP 9 - Save the Tableau-ready CSV
# ------------------------------------------------------------------

os.makedirs(os.path.dirname(TABLEAU_CSV), exist_ok=True)
df.to_csv(TABLEAU_CSV, index=False)
print("\nTableau-ready CSV saved -> " + TABLEAU_CSV)
print("  Rows    : " + str(len(df)))
print("  Columns : " + str(len(df.columns)))


# ------------------------------------------------------------------
# STEP 10 - Quick churn rate check across new groups
# ------------------------------------------------------------------

print("\nChurn rate by customer_risk_level:")
risk_summary = df.groupby("customer_risk_level")["churn_numeric"].mean().mul(100).round(1)
for level, rate in risk_summary.sort_values(ascending=False).items():
    print("  " + level + ": " + str(rate) + "%")

print("\nChurn rate by tenure_group:")
tenure_summary = df.groupby("tenure_group")["churn_numeric"].mean().mul(100).round(1)
for grp, rate in tenure_summary.items():
    print("  " + grp + ": " + str(rate) + "%")

print("\nChurn rate by monthly_charge_group:")
charge_summary = df.groupby("monthly_charge_group")["churn_numeric"].mean().mul(100).round(1)
for grp, rate in charge_summary.items():
    print("  " + grp + ": " + str(rate) + "%")

print("\nPhase 5 data preparation complete.")
