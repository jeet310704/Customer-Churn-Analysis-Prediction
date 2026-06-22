-- ============================================================
-- churn_analysis_queries.sql
-- Phase 3: SQL Churn Analysis Queries
-- Database : sql/customer_churn.db
-- Table    : customer_churn
-- ============================================================
-- Run these queries in any SQLite tool, or let
-- scripts/run_churn_sql_analysis.py execute them for you.
-- ============================================================


-- ------------------------------------------------------------
-- Q1. Total number of customers
-- ------------------------------------------------------------
SELECT COUNT(*) AS total_customers
FROM customer_churn;


-- ------------------------------------------------------------
-- Q2. Total churned customers
-- ------------------------------------------------------------
SELECT COUNT(*) AS total_churned
FROM customer_churn
WHERE churn = 'Yes';


-- ------------------------------------------------------------
-- Q3. Overall churn rate (as a percentage)
-- ------------------------------------------------------------
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS churn_rate_pct
FROM customer_churn;


-- ------------------------------------------------------------
-- Q4. Churn count and rate by gender
-- ------------------------------------------------------------
SELECT
    gender,
    COUNT(*)                                                        AS total,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)                 AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    )                                                               AS churn_rate_pct
FROM customer_churn
GROUP BY gender
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- Q5. Churn count and rate by contract type
-- ------------------------------------------------------------
SELECT
    contract_type,
    COUNT(*)                                                        AS total,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)                 AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    )                                                               AS churn_rate_pct
FROM customer_churn
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- Q6. Churn count and rate by payment method
-- ------------------------------------------------------------
SELECT
    payment_method,
    COUNT(*)                                                        AS total,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)                 AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    )                                                               AS churn_rate_pct
FROM customer_churn
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- Q7. Churn count and rate by internet service
-- ------------------------------------------------------------
SELECT
    internet_service,
    COUNT(*)                                                        AS total,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)                 AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    )                                                               AS churn_rate_pct
FROM customer_churn
GROUP BY internet_service
ORDER BY churn_rate_pct DESC;


-- ------------------------------------------------------------
-- Q8. Average monthly charges by churn status
-- ------------------------------------------------------------
SELECT
    churn,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customer_churn
GROUP BY churn
ORDER BY churn;


-- ------------------------------------------------------------
-- Q9. Average tenure by churn status
-- ------------------------------------------------------------
SELECT
    churn,
    ROUND(AVG(tenure), 2) AS avg_tenure_months
FROM customer_churn
GROUP BY churn
ORDER BY churn;


-- ------------------------------------------------------------
-- Q10. Average support calls by churn status
-- ------------------------------------------------------------
SELECT
    churn,
    ROUND(AVG(support_calls), 2) AS avg_support_calls
FROM customer_churn
GROUP BY churn
ORDER BY churn;


-- ------------------------------------------------------------
-- Q11. Top high-risk customer segments
--      Groups customers by contract type, payment method, and
--      internet service; ranks by churn rate descending.
-- ------------------------------------------------------------
SELECT
    contract_type,
    payment_method,
    internet_service,
    COUNT(*)                                                        AS total,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)                 AS churned,
    ROUND(
        100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*),
        2
    )                                                               AS churn_rate_pct
FROM customer_churn
GROUP BY contract_type, payment_method, internet_service
HAVING COUNT(*) >= 5              -- only show segments with enough data
ORDER BY churn_rate_pct DESC
LIMIT 10;


-- ------------------------------------------------------------
-- Q12. Customers with high monthly charges AND many support calls
--      (potential high-value customers at risk of leaving)
-- ------------------------------------------------------------
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


-- ------------------------------------------------------------
-- Q13. Customers with low tenure on a Month-to-Month contract
--      (newest, least committed customers - highest flight risk)
-- ------------------------------------------------------------
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
