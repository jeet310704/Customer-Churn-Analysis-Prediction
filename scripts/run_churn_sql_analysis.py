"""
run_churn_sql_analysis.py
Phase 3: Run SQL churn analysis queries against the SQLite database.

Connects to sql/customer_churn.db, runs every business question as a
SQL query, prints clear results to the terminal, and saves a full
summary to reports/sql_churn_analysis_summary.txt.

Run from the project root:
    python scripts/run_churn_sql_analysis.py
"""

import os
import sqlite3
import pandas as pd


# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

DB_PATH     = os.path.join("sql",     "customer_churn.db")
REPORT_PATH = os.path.join("reports", "sql_churn_analysis_summary.txt")


# ------------------------------------------------------------------
# Helper: dual-output writer (terminal + report file)
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

def run_query(conn, label, sql):
    """Execute one SQL query, print the result as a table, and log it."""
    log("\n--- " + label + " ---")
    df = pd.read_sql_query(sql, conn)
    log(df.to_string(index=False))
    return df


# ------------------------------------------------------------------
# Connect to the database
# ------------------------------------------------------------------

if not os.path.exists(DB_PATH):
    print("ERROR: Database not found at " + DB_PATH)
    print("Please run:  python scripts/create_churn_database.py  first.")
    exit(1)

conn = sqlite3.connect(DB_PATH)
log("Connected to: " + DB_PATH)


# ------------------------------------------------------------------
# Section 1 - Overview
# ------------------------------------------------------------------

section("SECTION 1 - CUSTOMER OVERVIEW")

run_query(conn, "Q1. Total number of customers",
    "SELECT COUNT(*) AS total_customers FROM customer_churn;"
)

run_query(conn, "Q2. Total churned customers",
    "SELECT COUNT(*) AS total_churned FROM customer_churn WHERE churn = 'Yes';"
)

run_query(conn, "Q3. Overall churn rate (%)",
    """
    SELECT
        ROUND(
            100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
            2
        ) AS churn_rate_pct
    FROM customer_churn;
    """
)


# ------------------------------------------------------------------
# Section 2 - Churn by category
# ------------------------------------------------------------------

section("SECTION 2 - CHURN BY CATEGORY")

run_query(conn, "Q4. Churn by gender",
    """
    SELECT
        gender,
        COUNT(*)                                                    AS total,
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)             AS churned,
        ROUND(
            100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
            2
        )                                                           AS churn_rate_pct
    FROM customer_churn
    GROUP BY gender
    ORDER BY churn_rate_pct DESC;
    """
)

run_query(conn, "Q5. Churn by contract type",
    """
    SELECT
        contract_type,
        COUNT(*)                                                    AS total,
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)             AS churned,
        ROUND(
            100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
            2
        )                                                           AS churn_rate_pct
    FROM customer_churn
    GROUP BY contract_type
    ORDER BY churn_rate_pct DESC;
    """
)

run_query(conn, "Q6. Churn by payment method",
    """
    SELECT
        payment_method,
        COUNT(*)                                                    AS total,
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)             AS churned,
        ROUND(
            100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
            2
        )                                                           AS churn_rate_pct
    FROM customer_churn
    GROUP BY payment_method
    ORDER BY churn_rate_pct DESC;
    """
)

run_query(conn, "Q7. Churn by internet service",
    """
    SELECT
        internet_service,
        COUNT(*)                                                    AS total,
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)             AS churned,
        ROUND(
            100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
            2
        )                                                           AS churn_rate_pct
    FROM customer_churn
    GROUP BY internet_service
    ORDER BY churn_rate_pct DESC;
    """
)


# ------------------------------------------------------------------
# Section 3 - Average metrics by churn status
# ------------------------------------------------------------------

section("SECTION 3 - AVERAGE METRICS BY CHURN STATUS")

run_query(conn, "Q8. Average monthly charges by churn status",
    """
    SELECT
        churn,
        ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
    FROM customer_churn
    GROUP BY churn
    ORDER BY churn;
    """
)

run_query(conn, "Q9. Average tenure by churn status",
    """
    SELECT
        churn,
        ROUND(AVG(tenure), 2) AS avg_tenure_months
    FROM customer_churn
    GROUP BY churn
    ORDER BY churn;
    """
)

run_query(conn, "Q10. Average support calls by churn status",
    """
    SELECT
        churn,
        ROUND(AVG(support_calls), 2) AS avg_support_calls
    FROM customer_churn
    GROUP BY churn
    ORDER BY churn;
    """
)


# ------------------------------------------------------------------
# Section 4 - High-risk segments and at-risk customers
# ------------------------------------------------------------------

section("SECTION 4 - HIGH-RISK SEGMENTS AND AT-RISK CUSTOMERS")

run_query(conn, "Q11. Top 10 high-risk customer segments (by contract, payment, internet)",
    """
    SELECT
        contract_type,
        payment_method,
        internet_service,
        COUNT(*)                                                    AS total,
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)             AS churned,
        ROUND(
            100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
            2
        )                                                           AS churn_rate_pct
    FROM customer_churn
    GROUP BY contract_type, payment_method, internet_service
    HAVING COUNT(*) >= 5
    ORDER BY churn_rate_pct DESC
    LIMIT 10;
    """
)

run_query(conn, "Q12. High-value at-risk customers (monthly charges > $80 AND support calls > 6)",
    """
    SELECT
        customer_id,
        monthly_charges,
        support_calls,
        tenure,
        contract_type,
        churn
    FROM customer_churn
    WHERE monthly_charges > 80
      AND support_calls   > 6
    ORDER BY monthly_charges DESC, support_calls DESC;
    """
)

run_query(conn, "Q13. New customers on Month-to-Month contracts (tenure <= 12 months)",
    """
    SELECT
        customer_id,
        tenure,
        contract_type,
        monthly_charges,
        support_calls,
        churn
    FROM customer_churn
    WHERE tenure        <= 12
      AND contract_type  = 'Month-to-Month'
    ORDER BY tenure ASC, support_calls DESC;
    """
)


# ------------------------------------------------------------------
# Section 5 - Key business insights
# ------------------------------------------------------------------

section("SECTION 5 - KEY BUSINESS INSIGHTS")

# Pull summary numbers to build insight statements
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM customer_churn")
total = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM customer_churn WHERE churn = 'Yes'")
churned = cur.fetchone()[0]

churn_rate = round(100.0 * churned / total, 2)

cur.execute("""
    SELECT contract_type, ROUND(100.0 * SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2)
    FROM customer_churn GROUP BY contract_type ORDER BY 2 DESC LIMIT 1
""")
top_contract, top_contract_rate = cur.fetchone()

cur.execute("""
    SELECT payment_method, ROUND(100.0 * SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2)
    FROM customer_churn GROUP BY payment_method ORDER BY 2 DESC LIMIT 1
""")
top_payment, top_payment_rate = cur.fetchone()

cur.execute("SELECT ROUND(AVG(monthly_charges),2) FROM customer_churn WHERE churn='Yes'")
avg_mc_churned = cur.fetchone()[0]

cur.execute("SELECT ROUND(AVG(monthly_charges),2) FROM customer_churn WHERE churn='No'")
avg_mc_retained = cur.fetchone()[0]

cur.execute("SELECT ROUND(AVG(tenure),1) FROM customer_churn WHERE churn='Yes'")
avg_tenure_churned = cur.fetchone()[0]

cur.execute("SELECT ROUND(AVG(tenure),1) FROM customer_churn WHERE churn='No'")
avg_tenure_retained = cur.fetchone()[0]

cur.execute("""
    SELECT COUNT(*) FROM customer_churn
    WHERE monthly_charges > 80 AND support_calls > 6 AND churn = 'Yes'
""")
high_risk_churned = cur.fetchone()[0]

cur.execute("""
    SELECT COUNT(*) FROM customer_churn
    WHERE tenure <= 12 AND contract_type = 'Month-to-Month' AND churn = 'Yes'
""")
new_mtm_churned = cur.fetchone()[0]

log("1. Overall churn rate is " + str(churn_rate) + "% (" + str(churned) + " of " + str(total) + " customers).")
log("2. " + top_contract + " contracts have the highest churn rate at " + str(top_contract_rate) + "%.")
log("3. " + top_payment + " is the riskiest payment method with a " + str(top_payment_rate) + "% churn rate.")
log("4. Churned customers pay $" + str(avg_mc_churned) + "/mo on average vs $" + str(avg_mc_retained) + "/mo for retained customers.")
log("5. Churned customers have an average tenure of " + str(avg_tenure_churned) + " months vs " + str(avg_tenure_retained) + " months for retained.")
log("6. " + str(high_risk_churned) + " high-value customers (charges > $80, calls > 6) have already churned.")
log("7. " + str(new_mtm_churned) + " new Month-to-Month customers (tenure <= 12 months) have churned - a key retention target.")


# ------------------------------------------------------------------
# Save report
# ------------------------------------------------------------------

section("SAVING REPORT")

os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("CUSTOMER CHURN ANALYSIS - SQL ANALYSIS SUMMARY REPORT\n")
    f.write("Phase 3: SQL Database and Queries\n")
    f.write("=" * 60 + "\n\n")
    f.write("\n".join(report_lines))

log("SQL analysis report saved -> " + REPORT_PATH)

conn.close()
log("Database connection closed.")
log("\nPhase 3 SQL analysis complete.")
