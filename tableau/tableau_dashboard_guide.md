# Tableau Dashboard Guide
## Customer Churn Analysis Dashboard

This guide is written for complete beginners. Every step tells you exactly
what to click, where to drag, and what you should see on screen. Follow each
section in order from top to bottom.

---

## Quick Overview — What You Will Build

You will build one dashboard with:
- 6 KPI cards along the top (key numbers at a glance)
- 9 charts showing churn patterns across customer segments
- 7 interactive filters so viewers can explore the data themselves

Total time: approximately 60-90 minutes if you follow each step carefully.

---

## Part 1 — Open Tableau and Connect to the Data

### Step 1 — Open Tableau

- If you have **Tableau Desktop**: open it from your Start Menu or desktop
  shortcut.
- If you are using **Tableau Public** (free): go to
  https://public.tableau.com and click "Download Tableau Public", install it,
  then open it.

When Tableau opens you will see the **Start Screen**. On the left side you
will see a panel called **Connect**.

---

### Step 2 — Connect to the CSV File

1. On the Start Screen, look at the left panel under the heading **Connect**.
2. Under "To a File", click **Text File**.
3. A file browser window will open.
4. Navigate to your project folder:
   `Customer Churn Analysis & Prediction / tableau /`
5. Click on **customer_churn_tableau.csv**
6. Click **Open**.

Tableau will now open the **Data Source tab** — a spreadsheet-like preview
of your data.

---

### Step 3 — Confirm the Data Loaded Correctly

On the Data Source tab you should see:

- A preview grid at the bottom of the screen showing rows of customer data
- Column headers across the top of the grid
- The filename `customer_churn_tableau.csv` shown in the left panel

**Check these things before continuing:**

1. **Row count** — look at the bottom-left of the grid. It should say
   approximately 700 rows.

2. **Column count** — scroll right across the grid. You should see 17 columns:

   `customer_id`, `gender`, `age`, `tenure`, `contract_type`,
   `payment_method`, `monthly_charges`, `total_charges`, `support_calls`,
   `internet_service`, `churn`, `churn_numeric`, `age_group`,
   `tenure_group`, `monthly_charge_group`, `support_call_group`,
   `customer_risk_level`

3. **Data types** — look at the small icons above each column name:
   - A small **Abc** icon means Tableau read it as text (correct for
     `customer_id`, `gender`, `churn`, `contract_type`, etc.)
   - A **#** icon means Tableau read it as a number (correct for
     `age`, `tenure`, `monthly_charges`, `churn_numeric`, etc.)

4. **Fix a data type if needed** — if `churn_numeric` shows **Abc** instead
   of **#**, click the **Abc** icon above that column and select
   **Number (whole)** to fix it.

Once everything looks correct, click the orange **Sheet 1** tab at the
very bottom of the screen. This takes you to your first worksheet where
you will start building.

---

## Part 2 — The Tableau Worksheet Layout

Before you build anything, understand the key areas on screen:

```
+-------------------+----------------------------------------+
|                   |   COLUMNS shelf (drag fields here)    |
|  Data panel       +----------------------------------------+
|  (your 17 columns |   ROWS shelf (drag fields here)        |
|  listed here)     +----------------------------------------+
|                   |                                        |
|                   |   CANVAS (your chart appears here)     |
|                   |                                        |
|  Marks card:      |                                        |
|  - Color          |                                        |
|  - Size           |                                        |
|  - Text           |                                        |
|  - Tooltip        |                                        |
|  - Detail         |                                        |
+-------------------+----------------------------------------+
```

- **Data panel (left side)** — lists all your columns. Blue fields are
  dimensions (categories like gender, contract type). Green fields are
  measures (numbers like monthly_charges, tenure).
- **Columns shelf (top)** — drag a field here to put it on the horizontal axis
- **Rows shelf (below Columns)** — drag a field here to put it on the
  vertical axis
- **Marks card (left, below Data panel)** — controls Color, Size, Text,
  and Tooltip for your chart. There is also a dropdown at the top of the
  Marks card where you change the chart type (Bar, Line, Text, etc.)
- **Canvas (centre)** — this is where your chart appears

---

## Part 3 — Create the Calculated Fields

Calculated fields are custom formulas you create once, then use in any chart.
You must create all 6 before building charts.

**How to open the calculated field editor:**
1. Click the **Analysis** menu at the very top of the screen
2. Click **Create Calculated Field...**
3. A small window appears with a name box at the top and a formula box below

Create each field below exactly as written.

---

### Calculated Field 1 — Churn Rate

**Why you need this:** `churn_numeric` is 1 for churned customers and 0 for
retained. When you average a column of 1s and 0s, the result is the
proportion that equals 1. So `AVG(churn_numeric)` = churn rate as a decimal
(e.g. 0.54 = 54%). This is the standard way to calculate a percentage in
Tableau when you have a 0/1 column.

1. Click **Analysis > Create Calculated Field**
2. In the **Name** box at the top, type exactly: `Churn Rate`
3. In the formula box, type exactly:
   ```
   AVG([churn_numeric])
   ```
4. Look at the bottom of the window — it should say "The calculation is
   valid." If it shows an error, check your spelling.
5. Click **OK**

After creating it, format it as a percentage:
1. In the Data panel on the left, find **Churn Rate** under Measures
2. Right-click it > **Default Properties** > **Number Format**
3. Select **Percentage**, set decimal places to **1**
4. Click **OK**

---

### Calculated Field 2 — Churned Customers

1. Click **Analysis > Create Calculated Field**
2. Name: `Churned Customers`
3. Formula:
   ```
   SUM([churn_numeric])
   ```
4. Click **OK**

This counts the total number of churned customers (sums all the 1s).

---

### Calculated Field 3 — Total Customers

1. Click **Analysis > Create Calculated Field**
2. Name: `Total Customers`
3. Formula:
   ```
   COUNT([customer_id])
   ```
4. Click **OK**

This counts the total number of rows (one row = one customer).

---

### Calculated Field 4 — Average Monthly Charges

1. Click **Analysis > Create Calculated Field**
2. Name: `Average Monthly Charges`
3. Formula:
   ```
   AVG([monthly_charges])
   ```
4. Click **OK**

Format it as currency:
1. Right-click **Average Monthly Charges** in the Data panel
2. **Default Properties > Number Format > Currency (Custom)**
3. Set Decimal places to **2**, prefix to **$**
4. Click **OK**

---

### Calculated Field 5 — Average Tenure

1. Click **Analysis > Create Calculated Field**
2. Name: `Average Tenure`
3. Formula:
   ```
   AVG([tenure])
   ```
4. Click **OK**

---

### Calculated Field 6 — Average Support Calls

1. Click **Analysis > Create Calculated Field**
2. Name: `Average Support Calls`
3. Formula:
   ```
   AVG([support_calls])
   ```
4. Click **OK**

You now have 6 custom calculated fields. You will see them appear in your
Data panel under Measures (they have a small equals sign icon next to them).

---

## Part 4 — Build the KPI Cards

A KPI card is a worksheet that shows a single large number. You will build
6 of them, one for each key metric. Each takes about 2 minutes.

**The pattern for every KPI card is the same:**
1. Create a new worksheet
2. Change the Mark type to **Text**
3. Drag one calculated field to the **Text** card
4. Format the number to look large and bold
5. Rename the worksheet

---

### KPI Card 1 — Total Customers

**Goal:** Show the number 700 in large bold text.

1. At the bottom of the screen, right-click the **Sheet 1** tab >
   click **Rename** > type `KPI - Total Customers`
2. In the **Marks card** (left side), click the dropdown at the top
   (it likely says "Automatic") and select **Text**
3. In the Data panel on the left, find **Total Customers** under Measures
4. Drag **Total Customers** and drop it onto the **Text** box in the
   Marks card
5. You should now see the number **700** on the canvas
6. To make it bigger: click the **Text** box in the Marks card, then
   click the three dots (**...**) next to the word "Text"
7. A text formatting window opens. Highlight the field name, increase
   the font size to **28** or larger, and tick **Bold**
8. Click **OK**
9. Add a title: double-click the grey title area at the top of the canvas
   (it may say "Sheet 1" or "KPI - Total Customers")
10. Type `Total Customers`, format it as 12pt, not bold
11. Click **OK**

The card should now show a large bold **700** with a small title above it.

---

### KPI Card 2 — Churned Customers

1. Click the **+** icon at the very bottom of the screen to create a new
   worksheet (or right-click any tab > **New Worksheet**)
2. Rename the tab: `KPI - Churned Customers`
3. In the Marks card dropdown, select **Text**
4. Drag **Churned Customers** to the **Text** box in the Marks card
5. You should see **378**
6. Enlarge the font: click the Text box > three dots > increase font to
   28pt, bold
7. Double-click the title area and type `Churned Customers`

---

### KPI Card 3 — Churn Rate

1. Create a new worksheet, rename it: `KPI - Churn Rate`
2. Marks card dropdown: select **Text**
3. Drag **Churn Rate** to the **Text** box in the Marks card
4. You should see **54.0%** (or similar — it will display as a percentage
   because you formatted it in Part 3)
5. Enlarge the font to 28pt, bold
6. Title: `Churn Rate`

**If you see a decimal like 0.54 instead of 54.0%:** The format did not
apply. Click the Text box > three dots > click the small dropdown next to
the field name > **Format** > set to **Percentage**, 1 decimal place.

---

### KPI Card 4 — Average Monthly Charges

1. New worksheet, rename: `KPI - Avg Monthly Charges`
2. Marks card: **Text**
3. Drag **Average Monthly Charges** to the **Text** box
4. You should see something like **$65.58**
5. Font: 28pt, bold
6. Title: `Avg Monthly Charges`

---

### KPI Card 5 — Average Tenure

1. New worksheet, rename: `KPI - Avg Tenure`
2. Marks card: **Text**
3. Drag **Average Tenure** to the **Text** box
4. You should see something like **36.04**
5. Font: 28pt, bold
6. Title: `Avg Tenure (Months)`

---

### KPI Card 6 — Average Support Calls

1. New worksheet, rename: `KPI - Avg Support Calls`
2. Marks card: **Text**
3. Drag **Average Support Calls** to the **Text** box
4. You should see something like **5.16**
5. Font: 28pt, bold
6. Title: `Avg Support Calls`

You now have 6 KPI worksheets. Check your tab bar at the bottom — you
should see all 6 KPI tabs plus any original sheets.

---

## Part 5 — Build the Charts

For each chart, create a new worksheet first. The pattern is always the
same: change the mark type, drag fields to Columns/Rows/Color/Text, then
format and label.

---

### Chart 1 — Churn Count by Churn Status

**What it shows:** A simple two-bar chart — how many customers churned (Yes)
versus how many stayed (No). This is the first chart any stakeholder will
want to see.

1. Create a new worksheet, rename it: `Churn Count by Status`
2. In the Marks card dropdown, select **Bar**
3. Find `churn` in the Data panel (it is a dimension — blue colour)
4. Drag `churn` to the **Columns** shelf
5. Find `Total Customers` in the Data panel (it is a measure — green colour)
6. Drag `Total Customers` to the **Rows** shelf
7. You should now see two bars — one for "No" and one for "Yes"
8. **Add colour:** drag `churn` from the Data panel onto the **Color** box
   in the Marks card. The two bars will now be different colours.
9. **Change the colours:**
   - Click the **Color** box in the Marks card
   - Click **Edit Colors**
   - Click **Yes** and change it to red: click the colour swatch, pick red
   - Click **No** and change it to steel blue: click the swatch, pick a
     blue colour
   - Click **OK** on both windows
10. **Add data labels:** click the **Label** box in the Marks card, tick
    **Show mark labels**
11. **Add a title:** double-click the title area and type `Churn Count by Status`

Your chart should show two bars — a blue "No" bar (322) and a red "Yes"
bar (378).

---

### Chart 2 — Churn Rate by Contract Type

**What it shows:** Which contract type has the highest churn rate. You
expect Month-to-Month to be the tallest bar.

1. New worksheet, rename: `Churn Rate by Contract Type`
2. Marks card: **Bar**
3. Drag `contract_type` to the **Columns** shelf
4. Drag `Churn Rate` to the **Rows** shelf
5. You should see three bars, one for each contract type
6. **Sort descending:** click the vertical axis label (it says "Churn Rate")
   then click the sort-descending icon in the toolbar (two lines with a
   downward arrow), or right-click the axis > Sort > Descending
7. **Add data labels:** Marks card > **Label** box > tick **Show mark labels**
8. **Format the axis as percentage:** right-click the left axis > **Format
   Axis** > change numbers to Percentage, 1 decimal place
9. **Add colour by value:** drag `Churn Rate` onto the **Color** box in the
   Marks card. This creates a colour gradient — darker bars mean higher churn.
10. Title: `Churn Rate by Contract Type`

Expected result: Month-to-Month bar at 65.4%, One Year at 44.4%, Two Year
at 33.8%.

---

### Chart 3 — Churn Rate by Payment Method

**What it shows:** Whether the payment method a customer uses predicts churn.
Electronic Check will be the tallest bar.

1. New worksheet, rename: `Churn Rate by Payment Method`
2. Marks card: **Bar**
3. Drag `payment_method` to **Columns**
4. Drag `Churn Rate` to **Rows**
5. Sort descending (same as Chart 2)
6. Add data labels
7. Format axis as percentage
8. Drag `Churn Rate` to **Color** for the gradient effect
9. Title: `Churn Rate by Payment Method`

**Tip — if the labels overlap:** right-click the Columns axis >
**Rotate Label** to angle the text, or drag the column header wider.

Expected result: Electronic Check at 66.1%, then Bank Transfer, Mailed
Check, and Credit Card below it.

---

### Chart 4 — Churn Rate by Internet Service

**What it shows:** Whether the type of internet service is linked to churn.

1. New worksheet, rename: `Churn Rate by Internet Service`
2. Marks card: **Bar**
3. Drag `internet_service` to **Columns**
4. Drag `Churn Rate` to **Rows**
5. Sort descending
6. Add data labels
7. Format axis as percentage
8. Title: `Churn Rate by Internet Service`

Expected result: Fiber Optic at 56.0%, DSL at 54.4%, No Internet at 48.9%.

---

### Chart 5 — Churn Rate by Tenure Group

**What it shows:** Whether newer customers (shorter tenure) churn at higher
rates than long-term customers.

1. New worksheet, rename: `Churn Rate by Tenure Group`
2. Marks card: **Bar**
3. Drag `tenure_group` to **Columns**
4. Drag `Churn Rate` to **Rows**
5. Add data labels
6. Format axis as percentage
7. **Sort the bars in natural order** (0-12 first, 49+ last):
   - Right-click the `tenure_group` pill in the Columns shelf
   - Click **Sort**
   - Choose **Manual**
   - Drag the items into this order from top to bottom:
     0-12 Months, 13-24 Months, 25-48 Months, 49+ Months
   - Click **OK**
8. Title: `Churn Rate by Tenure Group`

Expected result: 0-12 Months has the highest churn rate.

---

### Chart 6 — Churn Rate by Age Group

**What it shows:** Whether a customer's age is related to their likelihood
of churning.

1. New worksheet, rename: `Churn Rate by Age Group`
2. Marks card: **Bar**
3. Drag `age_group` to **Columns**
4. Drag `Churn Rate` to **Rows**
5. Add data labels
6. Format axis as percentage
7. **Sort in natural order** (same method as Chart 5):
   Manual sort: 18-25, 26-35, 36-45, 46-55, 56+
8. Title: `Churn Rate by Age Group`

---

### Chart 7 — Churn Rate by Customer Risk Level

**What it shows:** Validates the risk scoring logic — High Risk customers
should churn at a much higher rate than Low Risk customers.

1. New worksheet, rename: `Churn Rate by Risk Level`
2. Marks card: **Bar**
3. Drag `customer_risk_level` to **Columns**
4. Drag `Churn Rate` to **Rows**
5. Add data labels
6. Format axis as percentage
7. Sort descending (High Risk first)
8. **Assign specific colours by risk level:**
   - Drag `customer_risk_level` onto the **Color** box in the Marks card
   - Click the **Color** box > **Edit Colors**
   - Set **High Risk** to red
   - Set **Medium Risk** to orange
   - Set **Low Risk** to green
   - Click **OK**
9. Title: `Churn Rate by Customer Risk Level`

Expected result: High Risk 72.2%, Medium Risk 45.8%, Low Risk 3.4%.
This is a strong visual showing the risk model works correctly.

---

### Chart 8 — Average Monthly Charges by Churn Status

**What it shows:** Whether churned customers were paying more per month than
customers who stayed.

1. New worksheet, rename: `Avg Monthly Charges by Churn`
2. Marks card: **Bar**
3. Drag `churn` to **Columns**
4. Drag `Average Monthly Charges` to **Rows**
5. Drag `churn` to the **Color** box in the Marks card
   (use red for Yes, blue for No — same colours as Chart 1)
6. **Format the axis as currency:**
   Right-click the left axis > **Format Axis** > change to Currency ($),
   2 decimal places
7. Add data labels (click Label box > Show mark labels)
8. **Format data labels as currency too:**
   Click the Label box > click the three dots > click the field name
   dropdown > Format > Currency ($), 2 decimal places
9. Title: `Avg Monthly Charges by Churn`

Expected result: Yes (churned) bar at $68.47, No (retained) bar at $62.20.

---

### Chart 9 — Support Calls vs Churn (Stacked Bar)

**What it shows:** Of the customers in each support call volume tier, what
percentage churned? Customers who called support more should have a larger
red section in their bar.

1. New worksheet, rename: `Support Calls vs Churn`
2. Marks card: **Bar**
3. Drag `support_call_group` to **Columns**
4. Drag `Total Customers` to **Rows**
5. Drag `churn` to the **Color** box in the Marks card
6. The bars will now be stacked — the bottom portion is one churn value,
   the top portion is the other. Use red for Yes and blue for No.
7. **Sort the columns in natural order:**
   Right-click `support_call_group` in the Columns shelf > Sort > Manual >
   drag into order: 0-1 Calls, 2-3 Calls, 4+ Calls > OK
8. **Add percentage labels:**
   - Click the **Label** box in the Marks card
   - Tick **Show mark labels**
   - Under **Label Appearance**, change the dropdown from "All" to
     "Selected" if you want only specific labels, or leave on "All"
9. Title: `Support Calls vs Churn`

Expected result: The "4+ Calls" bar should have a noticeably larger red
(churned) section compared to the "0-1 Calls" bar.

---

## Part 6 — Add Filters to One Worksheet

Filters let dashboard viewers slice the data in real time. You only need to
add them to one worksheet — then you will apply them to all worksheets from
the dashboard.

Use the **Churn Rate by Contract Type** worksheet to add the filters.

1. Click on the `Churn Rate by Contract Type` tab at the bottom
2. In the Data panel on the left, find `gender`
3. Drag `gender` to the **Filters shelf** (it sits just above the Marks card)
4. A window pops up asking which values to include — tick **All** and
   click **OK**
5. Right-click the `gender` pill in the Filters shelf > click **Show Filter**
   — a filter control will appear on the right side of the worksheet
6. Repeat steps 2-5 for these fields:
   - `contract_type`
   - `payment_method`
   - `internet_service`
   - `age_group`
   - `tenure_group`
   - `customer_risk_level`

You should now see 7 filter controls on the right side of the worksheet.
You will connect these to all charts when you build the dashboard.

---

## Part 7 — Build the Dashboard

The dashboard is a single canvas where you arrange all your KPI cards,
charts, and filters together.

### Step 1 — Create the Dashboard

1. At the bottom of the screen, click the **New Dashboard** icon
   (it looks like a grid with a plus sign, to the right of the last
   worksheet tab)
2. A blank grey canvas appears
3. On the left side you will see two panels:
   - **Sheets** — lists all your worksheets to drag in
   - **Objects** — contains layout containers (Horizontal, Vertical,
     Text, Image, etc.)
4. Under **Size** on the left side, select **Fixed Size** from the
   dropdown and type **1200 x 900** (or choose Desktop Browser from
   the dropdown list)

---

### Step 2 — Add a Title

1. In the left panel under **Objects**, drag a **Text** object to the
   very top of the canvas
2. In the text editor that appears, type: `Customer Churn Analysis Dashboard`
3. Set font to **Arial, 20pt, Bold**, centre aligned
4. Click **OK**
5. Drag the bottom edge of the title to make it about 40px tall

---

### Step 3 — Add the KPI Cards (Top Row)

1. In the left panel under **Objects**, drag a **Horizontal** container
   onto the canvas, directly below the title
2. From the **Sheets** list, drag **KPI - Total Customers** into the
   horizontal container
3. Keep dragging all 6 KPI sheets into the same horizontal container,
   in this order:
   - KPI - Total Customers
   - KPI - Churned Customers
   - KPI - Churn Rate
   - KPI - Avg Monthly Charges
   - KPI - Avg Tenure
   - KPI - Avg Support Calls
4. They should sit side by side in a single row
5. Resize the row to be about 100-120px tall by dragging its bottom edge

**Tip:** If a KPI card is too wide or narrow, hover over the border
between two cards until you see a resize cursor, then drag to balance
the widths.

---

### Step 4 — Add Charts Row 1 (Churn by Category — Middle Row)

1. Drag a new **Horizontal** container below the KPI row
2. Drag these 3 sheets into it, left to right:
   - Churn Rate by Contract Type
   - Churn Rate by Payment Method
   - Churn Rate by Internet Service
3. Resize the row to about 200-220px tall

---

### Step 5 — Add Charts Row 2 (Customer Profiling — Lower Middle)

1. Drag another **Horizontal** container below the previous row
2. Drag these 3 sheets into it:
   - Churn Rate by Tenure Group
   - Churn Rate by Age Group
   - Churn Rate by Risk Level
3. Resize to about 200-220px tall

---

### Step 6 — Add Charts Row 3 (Detail Charts — Bottom)

1. Drag another **Horizontal** container at the bottom
2. Drag these 3 sheets into it:
   - Avg Monthly Charges by Churn
   - Support Calls vs Churn
   - Churn Count by Status
3. Resize to about 200-220px tall

---

### Step 7 — Add the Filters Panel (Right Side)

1. In the left panel under **Objects**, drag a **Vertical** container
   to the right side of the dashboard
2. Make it about 180px wide — drag its left edge to resize
3. Drag a **Text** object to the top of this vertical container and type
   `Filters` in 12pt bold
4. Now add the filter controls:
   - Click on any chart that has filters (e.g. Churn Rate by Contract Type)
   - You will see small filter cards appear on the right side of the
     worksheet view within the dashboard
   - Drag each filter card into your Filters vertical container

**Alternative method to add filters directly:**
   - On the dashboard, click any chart to select it
   - A small grey arrow appears in the top-right corner of that chart
   - Click the arrow > **Filters** > select a field name
   - A filter control appears on the dashboard

---

### Step 8 — Apply Filters to All Charts

This is the most important step. Right now your filters might only work
on one chart. You need to connect them to all charts at once.

1. Click on any filter control on the dashboard (e.g. the gender filter)
2. A small dropdown arrow appears at the top-right of the filter control
3. Click that arrow
4. Click **Apply to Worksheets**
5. Click **All Using This Data Source**
6. Repeat for every filter control

Now when a viewer changes the gender filter, all charts will update at once.

---

### Step 9 — Remove Worksheet Titles from Charts on the Dashboard

Chart titles inside the dashboard can look cluttered. A clean approach is
to use the chart's worksheet title (which you already set) rather than the
default header.

For each chart on the dashboard:
1. Right-click the chart
2. Click **Title**
3. If it is showing the worksheet name correctly, leave it
4. If you want to hide it, untick **Show Title**

---

### Step 10 — Final Formatting

1. **Dashboard background:** click anywhere on the blank canvas background
   > use the Format menu > Dashboard > choose white or light grey
2. **Add borders between charts:** Format menu > Dashboard > Sheet Borders
   > set to a thin light grey line
3. **Remove gridlines from charts** if they look cluttered:
   For each worksheet, go to Format > Lines > set Grid Lines to None
4. **Consistent colours:** make sure all charts use red (#E15759) for
   churned/Yes and blue (#4E79A7) for retained/No

---

## Part 8 — Final Layout Diagram

Here is what your finished dashboard should look like:

```
+------------------------------------------------------------------+
|        Customer Churn Analysis Dashboard (title bar)            |
+----------+----------+-----------+----------+----------+---------+
| Total    | Churned  | Churn     | Avg      | Avg      | Avg     |
| Customers| Customers| Rate      | Charges  | Tenure   | Support |
|   700    |   378    |  54.0%    | $65.58   | 36.0     |  5.16   |
+----------+----------+-----------+----------+----------+---------+
|                      |                     |                    |
| Churn Rate by        | Churn Rate by       | Churn Rate by      |
| Contract Type        | Payment Method      | Internet Service   |
|                      |                     |                    |
+----------------------+---------------------+--------------------+
|                      |                     |                    |
| Churn Rate by        | Churn Rate by       | Churn Rate by      |
| Tenure Group         | Age Group           | Risk Level         |
|                      |                     |                    |
+----------------------+---------------------+--------------------+
|                      |                     |                    |
| Avg Monthly Charges  | Support Calls       | Churn Count        |
| by Churn Status      | vs Churn            | by Status          |
|                      |                     |                    |
+-------------------------------------------------------+---------+
| Filters:                                              |         |
| [ Gender          ]  [ Contract Type      ]           | Filters |
| [ Payment Method  ]  [ Internet Service   ]           | panel   |
| [ Age Group       ]  [ Tenure Group       ]           |         |
| [ Risk Level      ]                                   |         |
+-------------------------------------------------------+---------+
```

---

## Part 9 — Colour Reference

Apply these colours consistently across all charts:

| Element | Colour | Hex Code |
|---|---|---|
| Churned / Yes | Red | #E15759 |
| Retained / No | Steel Blue | #4E79A7 |
| High Risk | Red | #E15759 |
| Medium Risk | Orange | #F28E2B |
| Low Risk | Green | #59A14F |
| KPI card background | Light grey | #F5F5F5 |
| Dashboard background | White | #FFFFFF |
| Chart borders | Light grey | #E0E0E0 |

---

## Part 10 — Save and Publish

**Tableau Public (free):**
1. Click **File > Save to Tableau Public**
2. If prompted, sign in with your Tableau Public account (free to create at
   public.tableau.com)
3. Give your workbook a name: `Customer Churn Analysis Dashboard`
4. Click Save
5. Your dashboard will open in a browser at your public Tableau profile
6. Copy the URL — you can add it to your portfolio, LinkedIn, or resume

**Tableau Desktop (paid):**
1. Click **File > Save**
2. Save as a `.twbx` file (a packaged workbook that includes the data)
3. Store the file in your project's `tableau/` folder

---

## Troubleshooting

**Problem: Churn Rate shows 0.54 instead of 54.0%**
Fix: The field is not formatted as a percentage. Right-click Churn Rate
in the Data panel > Default Properties > Number Format > Percentage, 1
decimal place.

**Problem: My bar chart shows lines instead of bars**
Fix: Click the Marks card dropdown and change from "Automatic" or "Line"
to "Bar".

**Problem: Filters are not updating all charts**
Fix: Click each filter dropdown arrow > Apply to Worksheets > All Using
This Data Source.

**Problem: The tenure_group or age_group bars are in the wrong order**
Fix: Right-click the field pill in Columns > Sort > Manual > drag to
the correct order.

**Problem: Data labels are showing too many decimal places**
Fix: Right-click a label on the chart > Format > change the number format
to match your preference (1 decimal for percentages, 2 for currency).

**Problem: I cannot find a calculated field I created**
Fix: Look under Measures in the Data panel. If it is still missing,
re-create it using Analysis > Create Calculated Field.

**Problem: Tableau Public is not showing my full data**
Fix: Tableau Public has a 15 million row limit. Your 700-row file is
well within this limit — if data appears missing, re-check your CSV
connection on the Data Source tab.
