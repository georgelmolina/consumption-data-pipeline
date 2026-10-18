

import pandas as pd


def clean_plant(df: pd.DataFrame) -> pd.DataFrame:

    # --- 1. Audit: rows where ALL columns are NaN ---
    all_nan_count = df.isna().all(axis=1).sum()
    print(f"Rows with all NaN values: {all_nan_count}")

    # --- 2. Drop rows where ALL columns are NaN ---
    df.dropna(how="all", inplace=True)

    # --- 3. Audit: rows with "Dosif. m3" in the first column ---
    dosif_count = (df.iloc[:, 0] == "Dosif. m3").sum()
    print(f"Rows with 'Dosif. m3' in first column: {dosif_count}")

    # --- 4. Drop repeated header rows ---
    for label in ["Dosif. m3", "Dosif. m3.1"]:
        df.drop(df[df.iloc[:, 0] == label].index, inplace=True)

    # --- 5. Drop last 2 rows (totals) ---
    df.drop(df.tail(2).index, inplace=True)

    # --- 6. Parse "date" column to datetime64 ---
    # dayfirst=True handles DD/MM/YYYY (Spanish standard).
    # errors="coerce" converts unparseable values to NaT instead of crashing.
    df["\n \n Fecha"] = pd.to_datetime(df["\n \n Fecha"], errors="coerce", dayfirst=True)

    # --- 7. Drop rows with erroneous future dates (year 2026+) ---
    # Keeps datetime64 dtype intact — required for Power BI time intelligence
    # and SQL Server date filtering. Formatting stays at the export layer.
    df = df[df["\n \n Fecha"].dt.year < 2026]

     # --- 6. Drop first column (delivery note number) ---
    df.drop(df.columns[0], axis=1, inplace=True)

    # --- 8. Reset index ---
    df.reset_index(drop=True, inplace=True)

    return df

