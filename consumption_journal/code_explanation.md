# Project: consumption_journal

## How many of the rows has "Dosif.m3" in the first column?

count = (P_A1_25.iloc[:, 0] == "Dosif.m3").sum()
print(f"Count of rows with 'Dosif.m3' in the first column: {count}")

✅

Here's the code to count rows with "Dosif.m3" in the first column:

```python
# How many of the rows has "Dosif.m3" in the first column?
count = (P_A1_25.iloc[:, 0] == "Dosif.m3").sum()
print(f"Count of rows with 'Dosif.m3' in the first column: {count}")
```

**What it does:**

- `P_A1_25.iloc[:, 0]` — selects the first column (index 0)
- `== "Dosif.m3"` — creates a boolean mask where True means the cell matches "Dosif.m3"
- `.sum()` — counts the True values (matches)

If you also want to see those rows:

```python
dosif_rows = P_A1_25[P_A1_25.iloc[:, 0] == "Dosif.m3"]
print(dosif_rows)
```

Here's the code to drop all rows with "Dosif.m3" in the first column:

```python
# Drop all rows with "Dosif.m3" in the first column
P_A1_25 = P_A1_25[P_A1_25.iloc[:, 0] != "Dosif.m3"]
```

Or if you prefer using `drop`:

```python
P_A1_25.drop(P_A1_25[P_A1_25.iloc[:, 0] == "Dosif.m3"].index, inplace=True)
```

**What it does:**

- First approach: keeps only rows where the first column is NOT equal to "Dosif.m3"
- Second approach: identifies matching rows and removes them in-place

The first approach is cleaner. You can verify the removal by checking the shape after:

```python
P_A1_25.shape
```

---

P_A1_25["date"] = pd.to_datetime(
    P_A1_25["date"].astype("string").str.strip(),
    format="%d/%m/%Y",
    errors="coerce"
)

---

P_A1_25["date"] = pd.to_datetime(P_A1_25["date"], format="%d-%m-%Y", errors="coerce")

✅

Great line to understand. Here is the detailed breakdown of what it does:

1. Left side of the assignment
   P_A1_25["date"] = ...
- P_A1_25 is your DataFrame.
- ["date"] points to the column named date.
- The equals sign means: replace that column with the result on the right side.

So this line overwrites the existing values in date.

2. Function being called
   pd.to_datetime(...)
- pd is pandas (from import pandas as pd).

- to_datetime is a pandas function that converts values into datetime type.

- It can convert text like 19-05-2026 into real dates that pandas can filter, sort, group, etc.
3. First argument inside the function
   P_A1_25["date"]
- This passes the current date column values into the converter.

- If the column is text/object before this line, pandas will try to parse each row into a datetime.
4. format parameter
   format="%d-%m-%Y"

This tells pandas the exact input pattern:

- %d = day (01 to 31)
- %m = month (01 to 12)
- %Y = 4-digit year (2026)

So pandas expects values like:

- 03-01-2025
- 19-05-2026

Important: this format describes the current input format, not necessarily the final display format.

5. errors parameter
   errors="coerce"

This controls what happens when a value cannot be parsed.

- coerce means: if parsing fails, pandas does not crash.
- Instead, invalid values become NaT (Not a Time), which is the datetime equivalent of missing value.

Without coerce, bad values could raise an exception and stop execution.

6. Final result in your DataFrame
   After running this line:
- date column dtype becomes datetime64[ns] (if conversion succeeds enough to infer datetime type).

- valid rows are real dates.

- invalid rows become NaT.

- your original text dates are replaced by datetime values.
7. Common confusion: format vs output display
   Even with format="%d-%m-%Y", pandas stores datetime values internally, not as fixed text.
   If later you want string output exactly as YYYY-MM-DD for export/display, that is a second step using dt.strftime("%Y-%m-%d").

Quick mental model:

- to_datetime = convert text to real date type
- strftime = format date type back to text pattern

If you want, I can now explain the exact difference in your notebook between:

1. Keeping date as datetime (best for analysis), and
2. Converting it to YYYY-MM-DD string (best for CSV/report output).

---

P_A1_25 = P_A1_25[P_A1_25["date"].dt.year != 2026]

Created 0 todos

```python
P_A1_25 = P_A1_25[P_A1_25["date"].dt.year != 2026]
```

**Line by line:**

- `P_A1_25["date"].dt.year` — extracts the year from each date value
- `!= 2026` — creates a boolean mask: `True` for rows to keep
- `P_A1_25[...]` — filters the DataFrame, keeping only `True` rows
- reassigned back to `P_A1_25` — overwrites the DataFrame without 2026 rows

---

zero_counts = (P_A1_25_clean != 0.0).sum()
zero_pct = zero_counts / len(P_A1_25_clean) * 100

pd.DataFrame({
    "zero_count": zero_counts,
    "zero_pct": zero_pct.round(2)
})

---

## File Path Strings in Python: `r"..."` vs `"\\..."`

**The Question:**
Why does this work:

```python
P_A1_25_clean.to_excel(r"C:\path\to\project\...", index=False)
```

But this also works:

```python
merged_df.to_excel("C:\\path\\to\\project\\...", index=False)
```

**The Answer: Raw Strings vs Escaped Backslashes**

### Method 1: Raw String `r"..."`

```python
path = r"C:\Users\User\Desktop\file.xlsx"
```

**How it works:**

- The `r` prefix tells Python: "treat this string LITERALLY"
- Backslashes are NOT interpreted as escape characters
- `\U` stays as `\U`, not converted to unicode
- Windows file paths work exactly as written

**Advantage:** More readable, matches Windows path directly

**Note:** The only limitation is you cannot end a raw string with a single backslash:

```python
# ❌ WRONG - raw string cannot end with backslash
r"C:\Users\file.xlsx\"

# ✅ CORRECT
r"C:\Users\file.xlsx"
```

### Method 2: Escaped Backslashes `"\\..."`

```python
path = "C:\\Users\\User\\Desktop\\file.xlsx"
```

**How it works:**

- No `r` prefix (regular string)
- Each backslash must be DOUBLED
- `\\` = one actual backslash in the final string
- Python parses escape sequences like `\n` (newline), `\t` (tab), `\\` (backslash)

**Disadvantage:** Less readable, more backslashes to type

**What happens if you forget to escape?**

```python
# ❌ WRONG - single backslash interpreted as escape
path = "C:\Users\User\Desktop\file.xlsx"
# Python tries to parse \U, \D, \f as escape sequences
# Results in unexpected characters or syntax error
```

**Why both exist:**
Both are valid, but `r"..."` is **preferred** for Windows paths because:

1. Easier to read and copy-paste from Windows Explorer
2. Fewer backslashes to type
3. Less error-prone
4. More Pythonic for file paths

**Professional Practice:**

```python
# ✅ BEST - use raw strings for file paths
input_file = r"C:\Users\User\Desktop\input.xlsx"
output_file = r"C:\Users\User\Desktop\output.xlsx"

# ✅ Also acceptable - use forward slashes (work on all OS)
input_file = "C:/Users/User/Desktop/input.xlsx"

# ❌ AVOID - hard to read and error-prone
input_file = "C:\\Users\\User\\Desktop\\input.xlsx"
```

**Cross-platform tip:**
Forward slashes `/` work on Windows, macOS, and Linux:

```python
path = "C:/Users/User/Desktop/file.xlsx"  # Works everywhere
```

**Summary:**

- Use `r"..."` for Windows paths → most readable
- Use `"C:/path"` for cross-platform code
- Avoid `"\\"` repetition unless necessary

---

# Inserting a new column and value.

# P_A1_24_clean["plant"] = "P_A1"

# Alternative way to inserting a column with values and the position too.

P_A1_24_clean.insert(1, "plant", "P_A1")

---

two ways to encode exportation. 

1. P_A1_24_clean.to_csv(cfg["P_A1_24_ready_csv_path"], index=False, encoding="utf-8-sig")
2. merged_df.to_csv(Path("..") / "data" / "export" / "consumption_dataset_ready.csv", index=False, encoding="utf-8")

file is loaded through a hardcoded relative path, for example "../../config/config.yaml".
Issue: this is fragile if the notebook is moved.
Fix: centralize path resolution or load paths from a reusable helper.

The way to encode a read file. 