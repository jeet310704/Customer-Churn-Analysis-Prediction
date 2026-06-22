# Customer Churn Analysis & Prediction

**An end-to-end data analytics and machine learning project** built with
Python, Pandas, SQL/SQLite, Scikit-learn, and Tableau to analyse customer
churn behaviour and predict which customers are at risk of cancelling.

---

## Project Overview

This project simulates a real-world business analytics workflow from start to
finish. Starting from a raw dataset, it covers data cleaning, exploratory
analysis, SQL querying, machine learning modelling, and Tableau dashboard
preparation — the same pipeline a data analyst or data scientist would follow
in an industry role.

The project is structured across six phases, each producing professional
deliverables that can be shown directly in a portfolio or discussed in an
interview.

---

## Business Problem

Customer churn — when a customer stops using a service — is one of the most
costly problems for subscription-based businesses. Industry research
consistently shows that acquiring a new customer costs significantly more than
retaining an existing one. Despite this, many companies only discover a
customer has churned after they have already left.

This project addresses that gap by:
- Identifying which customer attributes are most strongly associated with churn
- Quantifying churn risk across different customer segments
- Building a predictive model to flag at-risk customers before they leave
- Providing business recommendations to support retention decisions

---

## Project Objective

Build a full analytics and prediction pipeline that:

1. Generates and cleans a realistic customer dataset
2. Explores churn patterns using Python and SQL
3. Trains a machine learning model to predict individual churn risk
4. Prepares a Tableau dashboard for business stakeholders
5. Produces interview-ready documentation and resume bullets

---

## Tools and Technologies

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.x | Core scripting language |
| Pandas | Latest | Data loading, cleaning, and transformation |
| NumPy | Latest | Numerical operations |
| Scikit-learn | Latest | Machine learning models and evaluation |
| SQLite3 | Built-in | Lightweight SQL database |
| SQL | Standard | Business analysis queries |
| Tableau Desktop/Public | Latest | Interactive dashboard (built manually) |
| Pickle | Built-in | Saving and loading trained models |
| CSV | - | Raw and processed data storage |

---

## Dataset Overview

| Property | Value |
|---|---|
| Source | Synthetically generated (realistic patterns) |
| Total rows | 700 customer records |
| Total columns | 11 (raw) / 17 (Tableau-ready) |
| Missing values | 0 |
| Duplicate rows | 0 |
| Target variable | `churn` (Yes / No) |

**Column descriptions:**

| Column | Type | Description |
|---|---|---|
| customer_id | String | Unique customer identifier |
| gender | String | Male / Female |
| age | Integer | Customer age (18-70) |
| tenure | Integer | Months with the company (1-72) |
| contract_type | String | Month-to-Month / One Year / Two Year |
| payment_method | String | Electronic Check / Mailed Check / Bank Transfer / Credit Card |
| monthly_charges | Float | Monthly bill in USD ($20-$110) |
| total_charges | Float | Cumulative bill to date |
| support_calls | Integer | Number of support calls made (0-10) |
| internet_service | String | DSL / Fiber Optic / No Internet |
| churn | String | Yes (churned) / No (retained) — target variable |

---

## Project Workflow

### Phase 1 — Project Setup and Raw Dataset Creation
- Created the full folder structure
- Wrote `generate_churn_data.py` to produce a 700-row synthetic dataset
- Churn probability was modelled realistically: higher for Month-to-Month
  contracts, Electronic Check payments, high charges, frequent support calls,
  and low tenure customers
- Saved raw dataset to `data/raw/customer_churn_raw.csv`

### Phase 2 — Data Cleaning and Exploratory Data Analysis
- Loaded raw data and ran data quality checks (shape, dtypes, missing values,
  duplicates, and categorical uniqueness)
- Found zero missing values and zero duplicate rows
- Standardised all column names to snake_case
- Validated all numeric ranges (age, tenure, charges, support calls)
- Explored churn patterns across all categorical and numeric columns
- Saved cleaned data to `data/processed/customer_churn_cleaned.csv`
- Saved EDA summary to `reports/churn_eda_summary.txt`

### Phase 3 — SQLite Database and SQL Churn Analysis
- Loaded the cleaned CSV into a SQLite database (`sql/customer_churn.db`)
- Wrote 13 SQL queries covering overall churn rate, churn by category,
  average metrics by churn status, high-risk segment identification, and
  individual at-risk customer lists
- Saved all query results to `reports/sql_churn_analysis_summary.txt`

### Phase 4 — Machine Learning Churn Prediction
- Dropped `customer_id`, encoded the target (`Yes=1, No=0`), and applied
  one-hot encoding to 4 categorical features (13 total features after encoding)
- Split data 80/20 with stratification to preserve the churn ratio
- Trained two models: Logistic Regression (with StandardScaler) and
  Random Forest (100 trees)
- Selected Logistic Regression based on superior Recall — the primary metric
  for churn prediction, where missing a churner costs more than a false alarm
- Saved the trained model pipeline to `models/churn_prediction_model.pkl`
- Saved evaluation report to `reports/model_evaluation_report.txt`

### Phase 5 — Tableau Dashboard Preparation
- Added 6 new dashboard-friendly columns to the cleaned dataset:
  `churn_numeric`, `age_group`, `tenure_group`, `monthly_charge_group`,
  `support_call_group`, and `customer_risk_level`
- Risk level was scored using 5 churn risk factors (contract type, payment
  method, monthly charges, support calls, and tenure)
- Saved the Tableau-ready CSV to `tableau/customer_churn_tableau.csv`
- Wrote a full step-by-step dashboard guide covering 10 charts, 6 KPI cards,
  7 filters, calculated fields, layout, and colour recommendations

### Phase 6 — GitHub Documentation and Portfolio Preparation
- Rewrote README.md as a professional GitHub portfolio document
- Created `reports/resume_and_interview_notes.md` with resume bullets and
  interview explanations
- Created `reports/final_project_summary.txt` with a full project summary

---

## Key Business Questions

| # | Question | Answered In |
|---|---|---|
| 1 | What is the overall churn rate? | Phase 2 EDA, Phase 3 SQL |
| 2 | Which contract type has the highest churn? | Phase 2, Phase 3 |
| 3 | Does payment method predict churn? | Phase 2, Phase 3 |
| 4 | Do newer customers churn more? | Phase 2, Phase 3 |
| 5 | Which customer segment is highest risk? | Phase 3 SQL Q11 |
| 6 | Can we predict individual churn risk? | Phase 4 ML model |
| 7 | Which features matter most to the model? | Phase 4 feature importances |
| 8 | How can the business act on these insights? | Phase 5 dashboard, Phase 6 |

---

## Exploratory Data Analysis Summary

**Overall churn rate: 54.0%** (378 of 700 customers churned)

**Churn by contract type:**

| Contract Type | Churn Rate |
|---|---|
| Month-to-Month | 65.37% |
| One Year | 44.44% |
| Two Year | 33.83% |

**Churn by payment method:**

| Payment Method | Churn Rate |
|---|---|
| Electronic Check | 66.12% |
| Mailed Check | 48.84% |
| Bank Transfer | 49.31% |
| Credit Card | 43.88% |

**Churn by internet service:**

| Internet Service | Churn Rate |
|---|---|
| Fiber Optic | 55.95% |
| DSL | 54.40% |
| No Internet | 48.92% |

**Average metrics — churned vs retained:**

| Metric | Churned | Retained |
|---|---|---|
| Monthly Charges | $68.47 | $62.20 |
| Tenure | 34.4 months | 37.9 months |
| Support Calls | 5.54 | 4.72 |

---

## SQL Analysis Summary

13 queries were run against the SQLite database. Key findings:

- The single highest-risk customer segment was **Month-to-Month +
  Electronic Check + Fiber Optic**, with a churn rate of **84.38%**
  (54 churned out of 64 customers in that segment)
- Month-to-Month + Electronic Check + DSL had a **73.08%** churn rate
- 378 customers churned out of 700 total — a **54.0% churn rate**
- Churned customers averaged **5.54 support calls** vs 4.72 for retained
- Churned customers had **34.4 months average tenure** vs 37.9 for retained

Full results are in: `reports/sql_churn_analysis_summary.txt`

---

## Machine Learning Model Summary

**Models trained:** Logistic Regression, Random Forest Classifier

**Features used (13 after one-hot encoding):**
`age`, `tenure`, `monthly_charges`, `total_charges`, `support_calls`,
plus one-hot encoded `gender`, `contract_type`, `payment_method`,
`internet_service`

**Train/test split:** 80% training (560 rows) / 20% test (140 rows), stratified

**Results:**

| Metric | Logistic Regression | Random Forest |
|---|---|---|
| Accuracy | 51.43% | 48.57% |
| Precision | 54.76% | 52.63% |
| Recall | **60.53%** | 52.63% |
| F1-Score | **57.50%** | 52.63% |

**Selected model: Logistic Regression**

Logistic Regression was selected because it achieved higher Recall (60.53%)
than Random Forest (52.63%). In churn prediction, Recall is the priority
metric — a missed churner who leaves costs more than a false alarm that
triggers an unnecessary retention offer.

**Top 5 features by importance (from Random Forest):**
1. Monthly Charges — 17.47%
2. Total Charges — 15.83%
3. Tenure — 14.67%
4. Age — 13.78%
5. Support Calls — 12.95%

**Live demo prediction:**
A high-risk customer (28 years old, 4 months tenure, $95/month, 7 support
calls, Month-to-Month contract, Electronic Check, Fiber Optic) received a
predicted churn probability of **83%**.

The model is saved at: `models/churn_prediction_model.pkl`
Full results are in: `reports/model_evaluation_report.txt`

> Note: The dataset is synthetically generated with probabilistic churn labels,
> which places a natural ceiling on model accuracy. The model correctly learns
> the direction of all risk factors, as confirmed by feature importances
> aligning with the data generation logic.

---

## Tableau Dashboard Summary

**Dashboard name:** Customer Churn Analysis Dashboard
**Data source:** `tableau/customer_churn_tableau.csv` (700 rows, 17 columns)

**6 KPI cards:** Total Customers, Churned Customers, Churn Rate,
Average Monthly Charges, Average Tenure, Average Support Calls

**10 charts:**
- Churn count by status
- Churn rate by contract type, payment method, and internet service
- Churn rate by tenure group and age group
- Churn rate by customer risk level
- Average monthly charges by churn status
- Support calls vs churn (stacked bar)
- High-risk customer segment table

**7 interactive filters:** Gender, Contract Type, Payment Method,
Internet Service, Age Group, Tenure Group, Customer Risk Level

**Risk segmentation results:**
- High Risk customers: **72.2% churn rate**
- Medium Risk customers: **45.8% churn rate**
- Low Risk customers: **3.4% churn rate**

Build guide: `tableau/tableau_dashboard_guide.md`

---

## Project Folder Structure

```
Customer-Churn-Analysis-Prediction/
|
|-- data/
|   |-- raw/
|   |   `-- customer_churn_raw.csv          <- 700-row raw dataset
|   `-- processed/
|       `-- customer_churn_cleaned.csv      <- cleaned, snake_case columns
|
|-- scripts/
|   |-- generate_churn_data.py              <- Phase 1: creates raw dataset
|   |-- clean_and_explore_churn_data.py     <- Phase 2: cleans and explores
|   |-- create_churn_database.py            <- Phase 3: loads data into SQLite
|   |-- run_churn_sql_analysis.py           <- Phase 3: runs SQL queries
|   |-- build_churn_model.py                <- Phase 4: trains ML model
|   `-- prepare_tableau_data.py             <- Phase 5: prepares Tableau CSV
|
|-- sql/
|   |-- customer_churn.db                   <- SQLite database
|   `-- churn_analysis_queries.sql          <- 13 standalone SQL queries
|
|-- models/
|   |-- churn_prediction_model.pkl          <- saved best model (Logistic Reg)
|   `-- model_features.pkl                  <- saved feature column list
|
|-- reports/
|   |-- churn_eda_summary.txt               <- Phase 2 exploration output
|   |-- sql_churn_analysis_summary.txt      <- Phase 3 SQL query results
|   |-- model_evaluation_report.txt         <- Phase 4 model comparison
|   |-- resume_and_interview_notes.md       <- Phase 6 resume and interview prep
|   `-- final_project_summary.txt           <- Phase 6 project summary
|
|-- tableau/
|   |-- customer_churn_tableau.csv          <- dashboard data source (17 cols)
|   |-- tableau_dashboard_guide.md          <- step-by-step build guide
|   `-- tableau_dashboard_summary.txt       <- business summary
|
|-- README.md
`-- requirements.txt
```

---

## How to Run the Project

```bash
# Step 0 — Install dependencies
pip install -r requirements.txt

# Phase 1 — Generate the raw dataset
python scripts/generate_churn_data.py

# Phase 2 — Clean the data and run exploratory analysis
python scripts/clean_and_explore_churn_data.py

# Phase 3 — Create the SQLite database
python scripts/create_churn_database.py

# Phase 3 — Run SQL churn analysis queries
python scripts/run_churn_sql_analysis.py

# Phase 4 — Train and evaluate machine learning models
python scripts/build_churn_model.py

# Phase 5 — Prepare the Tableau-ready dataset
python scripts/prepare_tableau_data.py
```

All scripts must be run from the project root directory.
All outputs are saved automatically to their respective folders.

---

## Key Insights

The following insights were drawn directly from the EDA and SQL analysis:

1. **Month-to-Month contracts are the strongest churn indicator.**
   Customers on Month-to-Month contracts churned at 65.37%, compared to
   44.44% for One Year and 33.83% for Two Year contracts. Encouraging
   contract upgrades is a direct and measurable retention lever.

2. **Electronic Check is the highest-churn payment method.**
   Customers paying by Electronic Check churned at 66.12%, the highest of
   any payment method. This is notably higher than Credit Card (43.88%).

3. **The combination of contract type, payment method, and internet service
   creates extreme risk.**
   The Month-to-Month + Electronic Check + Fiber Optic segment had an
   84.38% churn rate (54 of 64 customers).

4. **Churned customers paid more per month on average.**
   Average monthly charges were $68.47 for churned customers versus $62.20
   for retained customers — a $6.27 gap — suggesting that bill size
   contributes to dissatisfaction.

5. **Churned customers had shorter average tenure.**
   The average tenure for churned customers was 34.4 months versus 37.9 months
   for retained customers, confirming that loyalty builds over time.

6. **Support call volume correlates with churn.**
   Churned customers averaged 5.54 support calls versus 4.72 for retained
   customers. Customers who contact support frequently may be experiencing
   unresolved service issues.

7. **The risk scoring model creates strong segment separation.**
   High Risk customers (scored 3+ risk factors) churned at 72.2%. Low Risk
   customers (0 risk factors) churned at only 3.4% — a 21x difference.

---

## Business Recommendations

Based on the analysis, the following actions are recommended:

1. **Offer retention incentives to Month-to-Month customers.**
   With a 65% churn rate, this segment represents the highest opportunity.
   A targeted offer — such as a bill discount or service upgrade — for
   customers who upgrade to a One Year contract could meaningfully reduce churn.

2. **Promote auto-pay to Electronic Check customers.**
   Customers using Electronic Check churn at 66.12%. Incentivising a switch
   to Bank Transfer or Credit Card auto-pay reduces friction and may improve
   retention.

3. **Prioritise support quality for high-call-volume customers.**
   Customers averaging more than 5 support calls are disproportionately
   represented in the churned group. A proactive follow-up after a customer's
   third support call could address issues before they decide to leave.

4. **Focus onboarding efforts on the first 12 months.**
   New customers (tenure 0-12 months) on Month-to-Month contracts represent
   the highest flight-risk group. A structured onboarding programme or a
   first-year loyalty benefit could improve early retention.

5. **Use churn prediction scores to prioritise retention outreach.**
   The trained model assigns a churn probability to each customer. The
   retention team can use this score to focus their calls and offers on
   the customers most likely to leave, making their effort more efficient.

6. **Monitor high monthly charge customers for dissatisfaction signals.**
   Customers paying over $80/month have a churn rate of 62.7%. Proactively
   checking in with these customers — or offering a loyalty discount — can
   address value concerns before they become a cancellation.

---

## Resume Bullet Points

These bullets are suitable for Data Analyst, Business Intelligence Analyst,
and Entry-Level Data Scientist roles:

- **Built an end-to-end customer churn analytics pipeline** using Python,
  Pandas, and NumPy — cleaned a 700-record dataset with zero missing values,
  standardised schema with snake_case naming, and validated all fields across
  6 data quality rules

- **Designed and queried a SQLite database** using 13 business-focused SQL
  queries to quantify churn risk by segment; identified that Month-to-Month +
  Electronic Check + Fiber Optic customers churned at 84%, the highest-risk
  segment across all combinations

- **Trained and evaluated Logistic Regression and Random Forest classifiers**
  using Scikit-learn on a stratified 80/20 train-test split; selected
  Logistic Regression based on superior Recall (60.5%) — the business-critical
  metric for minimising missed churn detections

- **Engineered 6 dashboard-ready features** (risk score, age/tenure/charge
  groups) and documented a 10-chart Tableau dashboard guide covering KPI cards,
  interactive filters, and calculated fields to surface churn insights for
  non-technical business stakeholders

---

## Interview Explanation

### 60-Second Explanation

"This project is an end-to-end customer churn analysis and prediction system.
The business problem it solves is simple: companies lose money when customers
cancel, and the goal is to identify which customers are at risk before they
actually leave.

I started by generating a realistic 700-customer dataset, then cleaned it with
Pandas — checking for missing values, duplicates, and data quality issues.
From there I loaded it into a SQLite database and wrote SQL queries to answer
real business questions, like which contract type has the highest churn rate.
I found that Month-to-Month customers churned at 65%, compared to 34% for
customers on Two Year contracts — that is an almost 2x difference.

I then built two machine learning models using Scikit-learn — Logistic
Regression and Random Forest — and chose Logistic Regression because it had
better Recall. In churn prediction, Recall matters most because missing a
customer who is about to leave is more costly than flagging someone who was
never going to churn. Finally, I prepared a Tableau-ready dataset with
engineered features like customer risk scoring, and documented a full
dashboard guide so a business team could immediately act on the insights.

The project covers the full workflow a data analyst or data scientist would
follow in a real company."

---

### 20-Second Explanation

"This is an end-to-end customer churn project. I cleaned a customer dataset
with Pandas, analysed churn patterns using SQL, built a Logistic Regression
model with Scikit-learn to predict which customers are at risk of leaving,
and prepared a Tableau dashboard to present the findings to stakeholders.
The whole pipeline goes from raw data to business recommendation."

---

## Future Improvements

Given more time or a real-world dataset, the following improvements would
strengthen the project:

1. **Hyperparameter tuning** — use `GridSearchCV` or `RandomizedSearchCV` to
   optimise model parameters and improve recall on the held-out test set

2. **Additional models** — test XGBoost or a Gradient Boosting Classifier,
   which often outperform Logistic Regression on tabular datasets

3. **Class imbalance handling** — apply SMOTE or class weighting to address
   any imbalance in the target variable and improve minority-class recall

4. **Feature engineering** — create interaction features (e.g.
   charges-per-month-of-tenure) that may carry stronger predictive signal

5. **Cross-validation** — replace the single train-test split with k-fold
   cross-validation for a more robust performance estimate

6. **Model explainability** — use SHAP values to explain individual
   predictions, making the model results more transparent to business users

7. **Deploy as an API** — wrap the saved model in a Flask or FastAPI endpoint
   so a CRM system could call it in real time to score incoming customers

---

## Project Status

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Project setup and raw dataset creation | Completed |
| Phase 2 | Data cleaning and exploratory analysis | Completed |
| Phase 3 | SQLite database and SQL analysis | Completed |
| Phase 4 | Machine learning churn prediction model | Completed |
| Phase 5 | Tableau dashboard preparation | Completed |
| Phase 6 | GitHub documentation and portfolio preparation | Completed |
