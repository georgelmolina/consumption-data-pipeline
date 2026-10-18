# Project: consumption_journal

NameError: name 'pd' is not defined
pandas is defined as pd in the first cell. Why do I still get an error?

Read `consumption_project/notebooks/functions.py`, lines 1 to 10

The problem is that functions.py doesn't import pandas. Your notebook imports it, but when the function runs, it can't find `pd` in its own namespace. Add the import at the top of functions.py: 

```
✅ Fixed.

Each Python file needs its own imports. Even though your notebook imports pandas, the function in functions.py can't access it unless the file imports it too. Re-run cell 5 and it should work now.

Made changes.

---

## 2026-05-27 — FileNotFoundError: config.yaml not found

**Issue:** Same path works in `00_testing.ipynb` but fails in `P_A1_25_cleaning.ipynb`. Suspected the libraries or the dataframe call were the problem ("calling the same dataframe from different indentation").

**Diagnosis:** The root cause was directory depth. `00_testing.ipynb` sits at `notebooks/`, so `../config/config.yaml` correctly resolves to `consumption_project/config/config.yaml`. `P_A1_25_cleaning.ipynb` sits one level deeper at `notebooks/Cleaning_25/`, so the same `../` only goes up to `notebooks/config/` — a path that does not exist.

**Solution:** Updated cell 2 in `P_A1_25_cleaning.ipynb` from `../config/config.yaml` to `../../config/config.yaml` to go up two directory levels.

**Learnings:** Relative paths in notebooks are resolved from the notebook's own directory, not from the project root. Each `../` goes up exactly one folder level. Whenever a notebook is placed inside a subfolder, every relative path must account for the extra level of nesting.

---

## 2026-05-27 — Red lines in functions.py: "Type of X is unknown"

**Issue (His Hypothesis):** Not stated — no clear hypothesis; assumed the code was broken.

**Diagnosis:** The errors were Pylance static type checker warnings, not real Python errors. Both functions (`clean_plant`, `pivot_and_clean_plant_columns`) accepted `df` with no type annotation. Pylance could not infer the type of `df`, so it flagged every method called on it (`.isna()`, `.drop()`, `.columns`, etc.) as "unknown type" — producing dozens of red highlights.

**Solution:** Added `pd.DataFrame` type annotations to both function signatures:
```python
def clean_plant(df: pd.DataFrame) -> pd.DataFrame:
def pivot_and_clean_plant_columns(df: pd.DataFrame) -> pd.DataFrame:
```

**Learnings:** Red lines in VS Code do not always mean broken code. Pylance performs static type analysis and warns when it cannot infer types — especially with generic parameter names like `df`. Adding type annotations silences these warnings and also improves IDE autocompletion. These are informational warnings; the code runs correctly without them.

---

## 2026-05-28 — ModuleNotFoundError: No module named 'functions'

**Issue (His Hypothesis):** Libraries and syntax are correct (same as `P_A1_25_cleaning.ipynb`, also at `notebooks/Cleaning_25/`). Assumed the imports were working.

**Diagnosis:** Python's module search path (stored in `sys.path`) includes the current notebook's directory and globally installed packages, but not parent directories by default. `P_A2_25_cleaning.ipynb` runs from `notebooks/Cleaning_25/`, while `functions.py` sits one level up at `notebooks/`. Python couldn't find `functions` because it wasn't searching `..`.

**Solution:** Added a cell before the import to extend Python's module search path:

```python
import sys
sys.path.insert(0, "..")  # Add parent directory to module search path
```

Then the import succeeds:

```python
from functions import clean_plant
```

**Learnings:** Local `.py` files in the same directory are found automatically, but files in parent/sibling directories require explicit path configuration. This is why globally installed packages (pandas, yaml, openpyxl) work anywhere—they're registered in the global site-packages. For local project modules scattered across subdirectories, always add the relative path to `sys.path` at the start of the notebook.
---

genial, gracias! ahora lo que ocurre es lo siguiente.  tengo duplicado  consumption_project aquí. En cambio, el directorio de carpetas  no ha cambiado

¡Qué buena captura! Lo que estás viendo ahí es el comportamiento clásico de VS Code cuando "guardas un Workspace" mientras tienes una carpeta abierta. No te preocupes, **tus carpetas en el disco duro están perfectas**, no se ha duplicado nada real.

Lo que ha pasado es que VS Code se ha confundido visualmente: está mostrando `consumption_project` como una **carpeta independiente** y, justo arriba, vuelve a mostrarlo todo porque está leyendo el archivo `consumption.code-workspace` como si fuera otro elemento del menú.

Vamos a limpiar ese árbol izquierdo para que te quede idéntico al de *products* en tres clics:

---

### Cómo quitar la duplicación visual

1. Baja hasta la **segunda** carpeta `consumption_project` (la de más abajo).
2. Haz **clic derecho** sobre ella.
3. En el menú que se despliega, busca y haz clic en la opción **`Remove Folder from Workspace`** (Quitar carpeta del espacio de trabajo).

> ⚠️ **¡Ojo!** Asegúrate de darle a **"Remove Folder..."** (Quitar) y **NUNCA a "Delete"** (Eliminar). "Remove" solo la borra de la vista de VS Code, mientras que "Delete" la enviaría a la papelera de reciclaje de Windows.

---

### ¿Por qué se ve el archivo de Workspace con el icono `{}` amarillo?

Como creaste el workspace desde dentro de la propia carpeta, el archivo se ha quedado viviendo dentro de `consumption_project`.

Si quieres que tu estructura quede impecable y ordenada como la de tu otra captura de Windows, lo ideal es que desde el explorador de archivos muevas el archivo `consumption.code-workspace` a tu carpeta general de **Workspaces** (junto al de products).

Una vez movido allí, cierras VS Code, haces doble clic en él desde Windows, ¡y verás el árbol de carpetas más limpio que una patena!

---

## PyArrow: The Parquet Engine

**What happened:**
When you ran `pd.read_parquet()`, you got an error:

```
ImportError: Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'...
```

This means pandas couldn't find a parquet reader/writer.

**What is PyArrow?**
PyArrow is a C++ library (with Python bindings) that:

- Reads and writes Apache Parquet files (a columnar data format)
- Provides high-speed data serialization
- Handles schema validation and type inference
- Integrates seamlessly with pandas DataFrames

**Why PyArrow is the professional choice (not fastparquet):**

1. **Performance**: PyArrow is faster due to C++ backend
2. **Maintenance**: Apache Foundation maintains it (industry standard)
3. **Integration**: Works with Spark, Duckdb, Polars, and other modern tools
4. **Type Safety**: Better schema handling and type compatibility
5. **Memory Efficiency**: Columnar format reduces I/O and storage
6. **Industry Standard**: Used in production data pipelines (AWS, GCP, Databricks)

**Alternative (fastparquet):**

- Python-only, slower
- Less active maintenance
- Legacy choice; avoid for new projects

**Why Parquet format itself?**

- **Compression**: Files are typically 10-20x smaller than CSV
- **Schema**: Type information is preserved (dates, integers, floats)
- **Speed**: Column-based reading is faster for analysis
- **Professional**: Used in data warehouses, data lakes, and enterprise ETL

**Installation:**

```bash
conda install -c conda-forge pyarrow
```

**Usage in your project:**

```python
# Load
df = pd.read_parquet("path/to/file.parquet")

# Save
df.to_parquet("path/to/file.parquet", compression='snappy')
```

**Key takeaway:**
For reproducible, professional data work, always use parquet files with pyarrow as your engine. It's cleaner than CSV, faster than pickle, and portable across all modern data tools.