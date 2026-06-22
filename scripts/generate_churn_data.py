"""
generate_churn_data.py
Generates a realistic synthetic customer churn dataset (700 rows)
and saves it to data/raw/customer_churn_raw.csv.

Run from the project root:
    python scripts/generate_churn_data.py
"""

import numpy as np
import pandas as pd
import os

# Seed for reproducibility
np.random.seed(42)

NUM_ROWS = 700

# ── 1. Base demographic and account features ─────────────────────────────────

customer_ids = [f"CUST-{str(i).zfill(4)}" for i in range(1, NUM_ROWS + 1)]

genders = np.random.choice(["Male", "Female"], size=NUM_ROWS)

ages = np.random.randint(18, 71, size=NUM_ROWS)

# Tenure in months (1–72); younger tenures skew toward higher churn later
tenures = np.random.randint(1, 73, size=NUM_ROWS)

contract_types = np.random.choice(
    ["Month-to-Month", "One Year", "Two Year"],
    size=NUM_ROWS,
    p=[0.55, 0.25, 0.20],   # most customers are on flexible contracts
)

payment_methods = np.random.choice(
    ["Electronic Check", "Mailed Check", "Bank Transfer", "Credit Card"],
    size=NUM_ROWS,
    p=[0.35, 0.25, 0.20, 0.20],
)

monthly_charges = np.round(np.random.uniform(20, 110, size=NUM_ROWS), 2)

# Total charges ≈ tenure × monthly (with small noise); capped sensibly
total_charges = np.round(
    tenures * monthly_charges * np.random.uniform(0.85, 1.05, size=NUM_ROWS), 2
)

support_calls = np.random.randint(0, 11, size=NUM_ROWS)  # 0–10 calls

internet_services = np.random.choice(
    ["Fiber Optic", "DSL", "No Internet"],
    size=NUM_ROWS,
    p=[0.45, 0.35, 0.20],
)

# ── 2. Realistic churn probability ───────────────────────────────────────────
# Each risk factor nudges the base probability up.

churn_prob = np.full(NUM_ROWS, 0.10)   # 10 % base churn rate

# Contract type risk
churn_prob += np.where(contract_types == "Month-to-Month", 0.30, 0.0)
churn_prob += np.where(contract_types == "One Year",       0.05, 0.0)

# Payment method risk
churn_prob += np.where(payment_methods == "Electronic Check", 0.15, 0.0)

# High monthly charges (above $70)
churn_prob += np.where(monthly_charges > 70, 0.12, 0.0)

# Many support calls (above 5)
churn_prob += np.where(support_calls > 5, 0.18, 0.0)

# Low tenure (less than 12 months)
churn_prob += np.where(tenures < 12, 0.15, 0.0)

# Internet service risk
churn_prob += np.where(internet_services == "Fiber Optic", 0.10, 0.0)

# Clip to [0, 1] so probabilities stay valid
churn_prob = np.clip(churn_prob, 0.0, 1.0)

# Draw binary churn outcome from each customer's probability
churn_flags = np.random.binomial(n=1, p=churn_prob)
churn_labels = np.where(churn_flags == 1, "Yes", "No")

# ── 3. Assemble DataFrame ────────────────────────────────────────────────────

df = pd.DataFrame({
    "Customer ID":      customer_ids,
    "Gender":           genders,
    "Age":              ages,
    "Tenure":           tenures,
    "Contract Type":    contract_types,
    "Payment Method":   payment_methods,
    "Monthly Charges":  monthly_charges,
    "Total Charges":    total_charges,
    "Support Calls":    support_calls,
    "Internet Service": internet_services,
    "Churn":            churn_labels,
})

# ── 4. Save to CSV ────────────────────────────────────────────────────────────

output_path = os.path.join("data", "raw", "customer_churn_raw.csv")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

# ── 5. Quick verification summary ────────────────────────────────────────────

print("Dataset generated successfully!")
print(f"  Rows    : {len(df)}")
print(f"  Columns : {len(df.columns)}")
print(f"  Saved to: {output_path}")
print(f"\nColumn names:\n  {list(df.columns)}")
print(f"\nChurn distribution:\n{df['Churn'].value_counts().to_string()}")
print(f"\nFirst 3 rows preview:\n{df.head(3).to_string(index=False)}")
