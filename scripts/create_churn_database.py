"""
create_churn_database.py
Phase 3: Load cleaned data into a SQLite database.

Reads the cleaned CSV and writes it into a SQLite database file so
every future analysis can run pure SQL instead of loading CSV files.

Run from the project root:
    python scripts/create_churn_database.py
"""

import os
import sqlite3
import pandas as pd


# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

CLEAN_CSV = os.path.join("data", "processed", "customer_churn_cleaned.csv")
DB_PATH   = os.path.join("sql", "customer_churn.db")
TABLE     = "customer_churn"


# ------------------------------------------------------------------
# Step 1 - Load the cleaned CSV
# ------------------------------------------------------------------

print("Loading cleaned dataset...")
df = pd.read_csv(CLEAN_CSV)
print("  Rows    : " + str(len(df)))
print("  Columns : " + str(len(df.columns)))
print("  Columns : " + str(list(df.columns)))


# ------------------------------------------------------------------
# Step 2 - Connect to (or create) the SQLite database
# ------------------------------------------------------------------

# sqlite3.connect() creates the file automatically if it doesn't exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
print("\nConnected to database: " + DB_PATH)


# ------------------------------------------------------------------
# Step 3 - Write the DataFrame into the database
# ------------------------------------------------------------------

# if_exists='replace' drops and recreates the table on every run
# so the script is safe to run more than once without creating duplicates
df.to_sql(TABLE, conn, if_exists="replace", index=False)
print("Table '" + TABLE + "' created and data inserted.")


# ------------------------------------------------------------------
# Step 4 - Verify the row count inside the database
# ------------------------------------------------------------------

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM " + TABLE)
db_rows = cursor.fetchone()[0]

print("\nVerification:")
print("  Rows in cleaned CSV      : " + str(len(df)))
print("  Rows loaded into database: " + str(db_rows))

if db_rows == len(df):
    print("  Row counts match - database loaded correctly.")
else:
    print("  WARNING: row count mismatch! Check for errors above.")


# ------------------------------------------------------------------
# Step 5 - Show a quick preview from the database
# ------------------------------------------------------------------

print("\nFirst 3 rows from the database:")
preview = pd.read_sql("SELECT * FROM " + TABLE + " LIMIT 3", conn)
print(preview.to_string(index=False))


# ------------------------------------------------------------------
# Step 6 - Show available columns (useful reminder for writing SQL)
# ------------------------------------------------------------------

cursor.execute("PRAGMA table_info(" + TABLE + ")")
cols = cursor.fetchall()
print("\nTable columns (name | type):")
for col in cols:
    print("  " + col[1] + " | " + col[2])

conn.close()
print("\nDatabase connection closed.")
print("Phase 3 database setup complete.")
