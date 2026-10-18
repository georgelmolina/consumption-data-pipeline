# Project: consumption_journal

✅

Lecture Note: `inplace=True` vs `inplace=False` in pandas

1. Core idea  
   `inplace` controls where the result of an operation is stored.
- `inplace=True`: modifies the existing DataFrame object directly.
- `inplace=False` (default in most methods): returns a new DataFrame (or Series), leaving the original unchanged unless you reassign.
2. Mental model  
   Think of two patterns:
- Mutate existing object:
  - “Change this object itself.”
- Create transformed copy:
  - “Give me a new object with the change.”
3. Why it matters  
- Data safety: With `inplace=False`, your original data remains available as a fallback.
- Reproducibility: Explicit reassignment (`df = df.drop(...)`) makes transformation flow clearer in ETL pipelines.
- Debugging: Easier to compare before/after versions when not mutating immediately.
- Chaining operations: `inplace=False` works better with method chaining and cleaner pipeline style.
- Side effects: `inplace=True` can accidentally affect downstream cells if the same object is reused.
4. Important practical note  
   In modern pandas workflows, many teams prefer `inplace=False` + explicit reassignment because it is clearer and safer.  
   Also, `inplace=True` does not always provide meaningful performance benefits in real workloads.

5. When to use each  
   Use `inplace=True` when:
- You are sure you no longer need the original object.
- You want concise mutation in quick exploratory steps.

Use `inplace=False` when:

- Building production or reusable pipelines.
- You want auditability and easier debugging.
- You need clean, predictable transformation steps.
6. Best-practice recommendation for your project  
   For professional ETL/data-engineering notebooks, prefer explicit reassignment:
- clearer lineage of transformations,
- lower risk of accidental side effects,
- easier code reviews and reproducibility.

If you want, I can draft a short team style rule for your notebook: when to allow `inplace=True` and when to ban it.

---

✅

Lecture Note: `drop=True` in `reset_index()`

1. What `drop=True` does  
   When you use:

```python
df.reset_index(drop=True)
```

pandas creates a new default integer index (`0, 1, 2, 3, ...`) and **discards the old index** instead of keeping it as a new column.

2. What happens without `drop=True`  
   If you run:

```python
df.reset_index()
```

pandas also rebuilds the index, but it **preserves the previous index** by inserting it into the DataFrame as a regular column, usually called `index`.

So the difference is:

- `drop=False` or omitted: old index is kept as a column

- `drop=True`: old index is removed completely
3. Why this is important  
   This matters because, after filtering or deleting rows, the old index often no longer has analytical value. If you keep it accidentally:
- you add a column that may be meaningless for the business process

- you can confuse row identifiers with real data

- you make the DataFrame less clean for later transformations

- joins, exports, and reports may include an unnecessary extra column
4. Professional interpretation  
   Use `drop=True` when the previous index is only a technical artifact and should not become part of the dataset.

This is common in ETL and data cleaning workflows, where the objective is to leave the DataFrame with:

- a clean sequential index

- only business-relevant columns

- no accidental metadata from previous filtering steps
5. Example

```python
import pandas as pd

df = pd.DataFrame({"A": [10, 20, 30]}, index=[0, 3, 6])

print(df)
```

Output:

```python
    A
0  10
3  20
6  30
```

If you do:

```python
df.reset_index()
```

Result:

```python
   index   A
0      0  10
1      3  20
2      6  30
```

If you do:

```python
df.reset_index(drop=True)
```

Result:

```python
    A
0  10
1  20
2  30
```

6. Why it is especially important in your notebook  
   In your case, after deleting rows, you want a clean sequential row index. The previous index values are not business data, so keeping them would only introduce noise. That is exactly why `drop=True` is the correct option.

7. Best-practice rule  
   Use `drop=True` when:
- the old index has no business meaning
- you want a clean final dataset
- you are preparing data for further transformation or export

Do not use `drop=True` when:

- the current index contains meaningful identifiers you may need later

If you want, I can also generate a second lecture note explaining the difference between `drop()` and `drop=True`, because they are related but not the same thing.

✅

Mostly **data cleaning**, with a small part of **data transformation**.

What you are doing so far:

- Removing fully empty rows: cleaning
- Removing rows like `"Dosif. m3"`: cleaning
- Removing summary/footer rows: cleaning
- Dropping a non-useful column: cleaning, assuming that column has no analytical value
- Resetting the index: cleaning/structuring
- Inspecting head, tail, shape, dtypes: validation, not transformation itself

When it becomes transformation:

- Renaming columns
- Changing date formats
- Converting data types
- Deriving new columns
- Reshaping the table
- Standardizing values for downstream analysis

Professional distinction:

- **Cleaning** means correcting, removing, or standardizing data quality issues.
- **Transformation** means changing the structure, format, or business meaning of the data so it is ready for analysis, modeling, or reporting.

So for your notebook’s current stage, the most accurate description is:

**You are primarily cleaning and validating the raw data, with some preparatory structuring steps before transformation.**

If you want, I can help you label each current notebook step as one of these:

1. Validation
2. Cleaning
3. Transformation
4. Business rule application

---

My prompt.

In the file "UniqueProducts_Dictionary_manual_ed" In the first column "raw_name" are the unique values of merged_df["product"] and in the second column "update_name" is where I typed manually the values for which raw_name. So, I need to map all values in the enitre merged_df based in this mapping/dictionary?

Can you improve this prompt more professionally?

IA improved prompt.
Original (paraphrased):
"In the file 'UniqueProducts_Dictionary_manual_ed', the first column 'raw_name' contains the unique values from merged_df['product'], and the second column 'updated_name' contains the manually corrected names. I need to map all values in the entire merged_df based on this mapping/dictionary."

Professional version:
"I have created a standardized product naming dictionary in 'UniqueProducts_Dictionary_manual_ed' containing:

raw_name column: the unique product names currently in merged_df['product']
updated_name column: the standardized product names I have manually defined
I need to apply this mapping to the entire merged_df dataset to replace all raw product names with their corresponding standardized names."

---

Empty cells have "NaN" value, is that ok for handling with SQL and power BI or is a better practice to fill empty cells with a proper word like for example "none"?

✅

`NaN` is fine for SQL Server — it imports as `NULL`, which is the correct standard for missing values in relational databases. Power BI also handles `NULL` natively.

Filling with `"none"` as a string is actually worse practice because:

- It is treated as a valid string value, not a missing value.
- Aggregations and filters in Power BI/SQL behave incorrectly — `"none"` would be counted as a category.
- `NULL` is the universal standard for "no value".

**Keep `NaN` — it becomes `NULL` in SQL, which is correct.**

docs/ currently mixes formal documentation (like Considerations.md, Discoveries.md) with ad-hoc exploration files. That's not a problem at this scale, but if the number of these reference Excels grows, grouping them under docs/references/ keeps the folder intent clear.

---

## Session Note — 2026-06-06 | `consumption_calculation.ipynb` — Volume comparison and product name audit

### What was done

Started building the core analytical layer inside `consumption_calculation.ipynb`, working from the two main datasets: `consumption_merged_ready` and `products_years`.

**1. Row count per month and year**  
Used `groupby` with `.dt.year` and `.dt.month` extractors on the `date` column, combined with `.size()` to count rows per period. Learned that `.dt` is the pandas datetime accessor — it lets you extract date parts (year, month, day, etc.) directly from a datetime column without additional imports.

**2. Volume sum per month and year (single dataset)**  
Applied the same `groupby` logic but aggregated with `["volume"].sum()` instead of `.size()`. The distinction is: `.size()` counts rows, `.sum()` aggregates a numeric column.

**3. Volume comparison table across both datasets**  
Built a single table merging `products_years` volume and `consumption_merged_ready` volume per month/year. Added two derived columns:

- `difference_m3`: absolute gap (products − consumption). Always positive, meaning products always records more volume than consumption.
- `difference_pct`: relative gap as a percentage of products volume, calculated as `(difference / products_volume_m3) * 100`. Gap ranges from ~5.7% to ~16.3%.

Used `pd.merge(..., how="outer")` to ensure no month is lost if one dataset has a period the other doesn't.

**4. Product name audit table**  
Built a `product_comparison` table with 138 unique products across both datasets. Used Python `set` operations (`|` for union) to collect all unique names, then created indicator columns showing where each product appears. The `match` column uses ✔/✘ to flag if a product name exists in both datasets exactly.

---

## Quick Note - Search Across Entire Workspace (VS Code)

If Ctrl+F only searches the current open file, use global search instead:

1. Press Ctrl+Shift+F to open Search view.
2. Type the target text (example: P_A1_25_clean_path).
3. Press Enter to search all files in the workspace.
4. Optional: in "files to include", use consumption_project/** to limit scope.
5. Use F4 and Shift+F4 to move between matches.

Key finding: several products appear only in one dataset — likely due to naming inconsistencies (e.g. `HM-20-15` vs `HM-20-B-15`, `H-100-B-20` vs `H-100/B/20`). This confirms the product name standardisation step is necessary before any joined calculation.

**5. Scrollable output trick**  
Learned that VS Code truncates notebook outputs beyond ~60 rows and shows a "scrollable" label. To force full display, wrap the `display()` call in `pd.option_context("display.max_rows", None)`. This overrides the row limit temporarily without permanently changing the pandas global setting.

### Key takeaways

- `.dt` accessor is the standard way to extract date parts from a pandas datetime column.
- `.size()` vs `.sum()` — always think: *do I want to count rows or aggregate values?*
- `pd.option_context` is the clean, non-destructive way to override pandas display settings per output.
- Product name mismatches between datasets are now confirmed and quantified — next step is the standardisation mapping.

---

## Quick Note - Publish-safe dictionary_path (merge notebook)

For public projects, avoid absolute local paths like `C:\Users\...` in notebooks.

Use a relative path in the dictionary-loading cell:

```python
# Load the dictionary file
dictionary_path = Path("../docs/UniqueProducts_Dictionary_manual_ed.xlsx")
# Read the Excel file with the mapping
product_dict_df = pd.read_excel(dictionary_path, sheet_name='Products', engine='openpyxl')
```

Why this is better:

1. No exposure of personal machine folder structure.
2. More portable for collaborators and GitHub reviewers.
3. Easier to run across different environments.

---

**Yes, CSV files are significantly better for AI, Machine Learning, and Data Engineering than XLS or XLSX files.** While Excel formats (`.xls`, `.xlsx`) are fantastic for human beings to look at, calculate, and color-code in an office setting, they are a nightmare for AI algorithms and automated data pipelines.

Here is exactly why CSV is the undisputed king when training AI models or feeding data into Python:

---

### 1. Zero Performance Overhead (Speed and Memory)

* **CSV (Comma-Separated Values):** Is just plain text. It has zero formatting, no colors, no font sizes, and no hidden metadata. Because it is so lightweight, Python tools like `pandas` or `Polars` can stream and load millions of rows of a CSV file into memory in seconds.
* **XLSX:** Is actually a zipped collection of complex XML files under the hood. For Python to read just *one* cell in an Excel sheet, it has to unzip the file, parse the XML structure, look up the style definitions, figure out if there's a formula, and then extract the value. This consumes **massive amounts of CPU and RAM**, making it painfully slow for large AI datasets.

---

### 2. No Hidden Formatting Traps (Data Integrity)

AI algorithms need absolute consistency. Excel is notorious for "guessing" data types and changing your data behind your back:

* If you have a product code like `00150`, Excel might automatically convert it to the number `150` and delete your leading zeros.
* If you have a concrete code like `C40-50`, Excel might accidentally interpret it as a date or a text formula.
* **CSV stores exactly what is written.** A `00150` stays `00150`. There are no automated assumptions, meaning your AI model gets clean, untampered data.

---

### 3. Open Standard vs. Proprietary Ecosystems

* **CSV** can be opened by *any* programming language, operating system (Linux, Windows, macOS), or AI framework (PyTorch, TensorFlow, Scikit-Learn) right out of the box without needing any special software.
* **XLSX** belongs to the Microsoft ecosystem. To read it in Python, you have to install third-party helper libraries like `openpyxl` or `xlrd`. If Microsoft updates the Excel file structure, your AI script could suddenly break.

---

### 4. Perfect for Git and Version Control

In AI development, you constantly track changes to your code and data.

* Because a CSV is plain text, version control tools like **Git** can show you the exact line-by-line changes (`diffs`) when a data scientist adds new rows or modifies a value.
* XLSX files are binary blobs. Git cannot read inside them, so if you change a single cell in Excel, Git just sees a completely different heavy binary file, ruining your version history.

---

### Summary: When to use which?

Think of it this way:

* Use **XLSX** when the data is meant for a **human business stakeholder** who needs dropdowns, pivot tables, and colored tabs.
* Use **CSV** (or even better production formats like **Parquet**) when the data is meant for a **machine, a Python script, or an AI model** that needs maximum speed, pure numbers, and rock-solid data integrity.

### Summary Comparison for AI and Coding

| Format               | Lightweight?            | Has Hierarchy/Structure?        | AI-Friendly?        | Best Use Case                                              |
|:-------------------- |:-----------------------:|:-------------------------------:|:-------------------:|:---------------------------------------------------------- |
| **`.docx` / `.pdf`** | ❌ No (Heavy binary/XML) | Yes (Visual)                    | ❌ No (Token waster) | Printing & sending official business contracts.            |
| **`.txt`**           | Yes (Ultra-light)       | ❌ No (Completely flat)          | 🤷 Muted            | Temporary scratchpads or raw system logs.                  |
| **`.md` (Markdown)** | **Yes (Ultra-light)**   | **Yes (Semantic/Text symbols)** | ** Yes (Perfect)**  | **Documentation, READMEs, AI prompts, and code comments.** |

By choosing Markdown for your project documentation, you are keeping your portfolio sleek, ensuring your AI prompts consume the fewest tokens possible, and practicing highly efficient engineering!