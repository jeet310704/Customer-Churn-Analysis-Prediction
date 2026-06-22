# Resume and Interview Notes
## Customer Churn Analysis & Prediction

---

## Resume Project Title

**Customer Churn Analysis & Prediction**
*Python | Pandas | SQL/SQLite | Scikit-learn | Tableau*

---

## Resume Bullet Points

Use these bullets on a CV or LinkedIn profile under a Projects section.
Choose 2-4 depending on available space.

---

**Bullet 1 — Data Cleaning and Engineering (Python/Pandas)**

Built an end-to-end customer churn analytics pipeline using Python and Pandas;
cleaned a 700-record dataset with zero missing values, standardised all column
names to snake_case, validated 6 data quality rules, and engineered 6
dashboard-ready features including a 5-factor customer risk score.

---

**Bullet 2 — SQL and Database Analysis (SQL/SQLite)**

Designed and queried a SQLite database using 13 business-focused SQL queries
to quantify churn risk across customer segments; identified that customers on
Month-to-Month contracts with Electronic Check payments and Fiber Optic
internet churned at 84% — the highest-risk segment in the dataset.

---

**Bullet 3 — Machine Learning (Scikit-learn)**

Trained and evaluated Logistic Regression and Random Forest classifiers using
Scikit-learn on a stratified 80/20 train-test split; selected Logistic
Regression based on superior Recall (60.5%), prioritising the detection of
at-risk customers over false-alarm minimisation.

---

**Bullet 4 — Business Insight and Visualisation (Tableau)**

Prepared a Tableau-ready dataset and authored a step-by-step dashboard guide
covering 6 KPI cards, 10 charts, 7 interactive filters, and calculated fields;
segmented customers into High/Medium/Low Risk tiers with a 21x churn rate
difference between the highest and lowest risk groups.

---

## One-Line Version (for tight CV space)

Built an end-to-end customer churn prediction project using Python, SQL,
Scikit-learn, and Tableau; cleaned and analysed 700 customer records,
identified an 84% churn rate in the highest-risk segment, and trained a
Logistic Regression model with 60.5% recall to flag at-risk customers.

---

## Tools and Skills Demonstrated

| Category | Tool / Skill |
|---|---|
| Language | Python 3 |
| Data manipulation | Pandas, NumPy |
| Database | SQLite3, SQL (13 queries) |
| Machine learning | Scikit-learn, Logistic Regression, Random Forest |
| Model evaluation | Accuracy, Precision, Recall, F1, Confusion Matrix |
| Feature engineering | One-hot encoding, risk scoring, binning |
| Visualisation prep | Tableau CSV preparation, dashboard guide authoring |
| Code quality | Modular scripts, inline comments, reproducible seeds |
| Reporting | Text-based summary reports saved programmatically |
| Version control | Project structured for GitHub |

---

## 20-Second Interview Explanation

Use this when asked "Tell me briefly about one of your projects."

"This is an end-to-end customer churn project. I cleaned a customer dataset
with Pandas, analysed churn patterns using SQL, built a Logistic Regression
model with Scikit-learn to predict which customers are at risk of leaving,
and prepared a Tableau dashboard to present the findings to stakeholders.
The whole pipeline goes from raw data to business recommendation."

---

## 60-Second Interview Explanation

Use this when asked "Walk me through one of your projects" in a technical
interview or when you have more time to explain.

"This project is an end-to-end customer churn analysis and prediction system.
The business problem it solves is simple: companies lose money when customers
cancel, and the goal is to identify which customers are at risk before they
actually leave.

I started by generating a realistic 700-customer dataset, then cleaned it
with Pandas — checking for missing values, duplicates, and data quality
issues. From there I loaded it into a SQLite database and wrote SQL queries
to answer real business questions, like which contract type has the highest
churn rate. I found that Month-to-Month customers churned at 65%, compared
to 34% for customers on Two Year contracts.

I then built two machine learning models using Scikit-learn — Logistic
Regression and Random Forest — and chose Logistic Regression because it had
better Recall. In churn prediction, Recall matters most because missing a
customer who is about to leave costs more than flagging someone who was never
going to churn. Finally, I prepared a Tableau-ready dataset with engineered
features like customer risk scoring, and documented a full dashboard guide so
a business team could immediately act on the insights.

The project covers the full workflow a data analyst or data scientist would
follow in a real company."

---

## Common Interview Follow-Up Questions

**Q: Why did you choose Logistic Regression over Random Forest?**

"I prioritised Recall as the key metric because in churn prediction, a false
negative — missing a customer who churns — is more costly than a false
positive. The Logistic Regression model achieved 60.5% Recall versus 52.6%
for Random Forest, so it was the better choice for this business objective."

---

**Q: Why is Recall more important than Accuracy for churn prediction?**

"Accuracy treats all errors equally, but in churn the costs are asymmetric.
If I miss a customer who is about to churn, they leave and the company loses
revenue with no chance to intervene. If I flag a customer who was going to
stay anyway, the worst case is they receive an unnecessary retention offer.
That is a much smaller cost, so I optimise for Recall — catching as many
true churners as possible."

---

**Q: How did you validate that your SQL results were correct?**

"I cross-checked the SQL query results against the Pandas EDA output from
Phase 2. Both used the same underlying dataset. The aggregate numbers —
churn rate, average charges, churn by contract type — matched exactly across
both approaches, which confirmed the SQL was correct."

---

**Q: What would you improve if you had more time?**

"Three things. First, I would apply hyperparameter tuning with GridSearchCV
to improve model performance. Second, I would test XGBoost, which often
outperforms Logistic Regression on tabular data. Third, I would add SHAP
values to explain individual predictions to non-technical stakeholders —
so instead of just saying a customer has a 78% churn probability, I could
show which factors drove that score."

---

**Q: What does your customer risk score actually measure?**

"It counts how many of five known churn risk factors apply to each customer:
Month-to-Month contract, Electronic Check payment, monthly charges above $70,
four or more support calls, and tenure of 12 months or less. Each factor adds
one point. A score of three or more is High Risk, one or two is Medium Risk,
and zero is Low Risk. High Risk customers had a 72.2% churn rate in the data,
compared to 3.4% for Low Risk — a clear and explainable separation."

---

## Key Numbers to Remember for Interviews

| Fact | Number |
|---|---|
| Total customers | 700 |
| Overall churn rate | 54.0% |
| Month-to-Month churn rate | 65.37% |
| Two Year contract churn rate | 33.83% |
| Electronic Check churn rate | 66.12% |
| Highest-risk segment churn rate | 84.38% (MTM + E-Check + Fiber Optic) |
| Avg monthly charge — churned | $68.47 |
| Avg monthly charge — retained | $62.20 |
| Model selected | Logistic Regression |
| Model Recall | 60.53% |
| Model F1-Score | 57.50% |
| High Risk churn rate | 72.2% |
| Low Risk churn rate | 3.4% |
| Total features in model | 13 (after one-hot encoding) |
| Train/test split | 80% / 20% |
