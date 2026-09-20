# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page Streamlit dashboard that shows total sales, total orders, a monthly sales trend, and sales by category and by region from `data/sales-data.csv`.

**Architecture:** `data.py` holds pure pandas functions (load and validate the CSV, plus every calculation) with pytest tests and no Streamlit imports. `app.py` is a thin Streamlit page that calls those functions and draws two KPI cards and three Plotly charts. Bad data raises a plain-English `DataError` that `app.py` shows with `st.error`.

**Tech Stack:** Python (plain `venv/`), Streamlit, pandas, Plotly, pytest.

**Spec:** `docs/superpowers/specs/2026-09-19-sales-dashboard-design.md` (requirements: `prd/ecommerce-analytics.md`; milestone board: `TASKS.md`)

## Global Constraints

- Work on the current branch `feature/sales-dashboard`. Do NOT create a git worktree or another branch.
- Plain Python virtual environment in `venv/` (already in `.gitignore`), dependencies in `requirements.txt`. No uv, no conda.
- Run Python tools as `./venv/Scripts/python -m <tool>` (for example `./venv/Scripts/python -m pytest`). This needs no activation and works in both PowerShell and Git Bash.
- `requirements.txt` uses minimum versions: `streamlit>=1.40`, `pandas>=2.2`, `plotly>=5.24`, `pytest>=8`.
- Data calculations live only in `data.py` (no Streamlit imports there) and are covered by pytest tests in `tests/test_data.py`.
- Two modules only: `data.py` and `app.py`. Chart code stays inline in `app.py`.
- Trend chart is monthly. Charts use one accent color, clear titles and axis labels, and `$` tooltips with exact values.
- Bad or missing data fails loudly with `DataError`; never silently clean data.
- Keep the code simple and readable, with short comments, so the owner can follow it.
- Every commit message starts with the milestone ID, for example `TASK-3: Add KPI cards`, and ends with the trailer `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` (pass it as a second `-m`).
- Do NOT edit `TASKS.md`. The owner ticks the acceptance criteria, fills in each `Commit:` line and moves milestones to Done.
- Deployment (Plan Task G) is executed by the owner from `main` after the merge. Agents stop before it.

## How this plan is numbered

Plan tasks are lettered **A to G** and their steps are `A.1`, `A.2`, and so on. That keeps them separate from the milestone IDs **TASK-1 to TASK-7** in `TASKS.md`. Every plan task names the milestone it belongs to.

| Plan task | Milestone | What it delivers |
|-----------|-----------|------------------|
| A | TASK-1 | `venv/`, `requirements.txt`, `pytest.ini`, placeholder `app.py` |
| B | TASK-2 | `data.py` with `DataError` and `load_sales`, plus tests; app loads data |
| C | TASK-3 | `total_sales`, `total_orders`, KPI cards |
| D | TASK-4 | `monthly_sales`, trend chart |
| E | TASK-5 | `sales_by_category`, `sales_by_region`, two bar charts |
| F | TASK-6 | Full verification, cross-check against the CSV, polish |
| G | TASK-7 | Deployment to Streamlit Community Cloud (**owner executes**) |

---

### Plan Task A: Environment setup and project skeleton (milestone: TASK-1)

**Files:**
- Create: `requirements.txt`, `pytest.ini`, `app.py`
- Create (git-ignored, not committed): `venv/`
- Also committed in this task: `docs/superpowers/specs/2026-09-19-sales-dashboard-design.md`, `docs/superpowers/plans/2026-09-19-sales-dashboard.md`

**Interfaces:**
- Consumes: nothing.
- Produces: a working `venv/` with all dependencies, and `app.py` that Plan Task B replaces.

- [ ] **Step A.1: Create the virtual environment**

Run from the repo root:

```bash
python -m venv venv
./venv/Scripts/python --version
```

Expected: prints a Python version of 3.11 or higher (the owner's machine has 3.14.x).

- [ ] **Step A.2: Write `requirements.txt` and install**

Create `requirements.txt`:

```
streamlit>=1.40
pandas>=2.2
plotly>=5.24
pytest>=8
```

Run:

```bash
./venv/Scripts/python -m pip install -r requirements.txt
./venv/Scripts/python -m pip list
```

Expected: install succeeds, and `pip list` shows streamlit, pandas, plotly and pytest. If any package fails to install, stop and report the exact error to the owner. Do not change Python versions or switch tools.

- [ ] **Step A.3: Write `pytest.ini`**

This lets tests in `tests/` do `import data` from the repo root.

```
[pytest]
pythonpath = .
testpaths = tests
```

- [ ] **Step A.4: Write the placeholder `app.py`**

```python
"""ShopSmart Sales Dashboard.

Run locally with:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

st.title("ShopSmart Sales Dashboard")
st.info("Dashboard coming soon.")
```

- [ ] **Step A.5: Verify the app runs without errors**

Check the script runs headlessly:

```bash
./venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); print('exceptions:', len(at.exception))"
```

Expected: `exceptions: 0`

Then check the real server starts. Start it in the background, wait a few seconds, query its health endpoint, then stop it:

```bash
./venv/Scripts/python -m streamlit run app.py --server.headless true --server.port 8599
```

In a second command: `curl -s http://localhost:8599/_stcore/health`. Expected: `ok`. Stop the background server afterwards.

- [ ] **Step A.6: Verify the project structure**

```bash
git status --short
```

Expected: `requirements.txt`, `pytest.ini`, `app.py` and the two `docs/` files show as untracked, and `venv/` does not appear (it is git-ignored). `data/sales-data.csv` is already tracked.

- [ ] **Step A.7: Commit**

```bash
git add requirements.txt pytest.ini app.py docs/superpowers/specs/2026-09-19-sales-dashboard-design.md docs/superpowers/plans/2026-09-19-sales-dashboard.md
git commit -m "TASK-1: Set up environment and project skeleton" -m "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step A.8: Milestone check (TASK-1 acceptance criteria)**

- Python 3.11+ environment with all four packages installed, and `requirements.txt` lists Streamlit, Plotly, Pandas (and pytest): done in A.1 and A.2.
- Project structure has `app.py` and `data/sales-data.csv`: done in A.4 and A.6.
- `streamlit run app.py` starts and shows the placeholder without errors: done in A.5.

Hand-off: tell the owner TASK-1 is ready for them to tick, add the `Commit:` hash to, and move to Done.

---

### Plan Task B: Data loading and basic structure (milestone: TASK-2)

**Files:**
- Create: `data.py`, `tests/test_data.py`
- Modify: `app.py` (replace the placeholder with data loading and error handling)

**Interfaces:**
- Consumes: `data/sales-data.csv`; `pytest.ini` from Plan Task A.
- Produces (used by every later plan task):
  - `data.DataError` (subclass of `ValueError`)
  - `data.load_sales(path) -> pandas.DataFrame` with columns `date` (datetime), `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount` (numbers). Raises `DataError` on any problem.
  - In `app.py`: the variable `sales` (the loaded DataFrame), the constant `DATA_FILE`, and the `get_sales()` cached loader.

- [ ] **Step B.1: Write the failing tests**

Create `tests/test_data.py`:

```python
"""Tests for data.py. Run from the project root with:  pytest"""

from pathlib import Path

import pandas as pd
import pytest

import data

REAL_CSV = Path(__file__).parent.parent / "data" / "sales-data.csv"
HEADER = "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
GOOD_ROW = "2024-01-03,ORD-1,Phone Case,Accessories,South,3,24.99,74.97\n"


def write_csv(tmp_path, text):
    """Write text to a temporary CSV file and return its path."""
    path = tmp_path / "sales.csv"
    path.write_text(text)
    return path


# ---- load_sales: happy path ----


def test_load_sales_reads_real_file_with_expected_shape():
    df = data.load_sales(REAL_CSV)
    assert len(df) == 482
    assert df["category"].nunique() == 5
    assert df["region"].nunique() == 4


def test_load_sales_converts_column_types(tmp_path):
    df = data.load_sales(write_csv(tmp_path, HEADER + GOOD_ROW))
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert pd.api.types.is_numeric_dtype(df["quantity"])
    assert pd.api.types.is_numeric_dtype(df["unit_price"])
    assert pd.api.types.is_numeric_dtype(df["total_amount"])


# ---- load_sales: bad data fails loudly ----


def test_load_sales_missing_file(tmp_path):
    with pytest.raises(data.DataError, match="not found"):
        data.load_sales(tmp_path / "nope.csv")


def test_load_sales_empty_file(tmp_path):
    with pytest.raises(data.DataError, match="no sales rows"):
        data.load_sales(write_csv(tmp_path, ""))


def test_load_sales_header_only(tmp_path):
    with pytest.raises(data.DataError, match="no sales rows"):
        data.load_sales(write_csv(tmp_path, HEADER))


def test_load_sales_missing_column_is_named_in_error(tmp_path):
    text = (
        "date,order_id,product,category,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-1,Phone Case,Accessories,3,24.99,74.97\n"
    )
    with pytest.raises(data.DataError, match="region"):
        data.load_sales(write_csv(tmp_path, text))


def test_load_sales_bad_date(tmp_path):
    row = GOOD_ROW.replace("2024-01-03", "not-a-date")
    with pytest.raises(data.DataError, match="date"):
        data.load_sales(write_csv(tmp_path, HEADER + row))


def test_load_sales_non_numeric_amount(tmp_path):
    row = GOOD_ROW.replace("74.97", "abc")
    with pytest.raises(data.DataError, match="total_amount"):
        data.load_sales(write_csv(tmp_path, HEADER + row))
```

- [ ] **Step B.2: Run the tests to verify they fail**

Run: `./venv/Scripts/python -m pytest -v`
Expected: collection error (`ImportError` / `ModuleNotFoundError`) because `data.py` does not exist yet.

- [ ] **Step B.3: Write `data.py`**

```python
"""Load and calculate sales data for the ShopSmart dashboard.

No Streamlit in this file: these are plain functions, so they are easy to test.
"""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "total_amount",
]
NUMBER_COLUMNS = ["quantity", "unit_price", "total_amount"]


class DataError(ValueError):
    """Raised when the sales CSV is missing or not in the expected format."""


def load_sales(path):
    """Read the sales CSV, check it, and return a DataFrame with proper types."""
    path = Path(path)
    if not path.exists():
        raise DataError(f"Sales file not found: {path}")

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise DataError(f"{path.name} contains no sales rows.") from None
    if df.empty:
        raise DataError(f"{path.name} contains no sales rows.")

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise DataError(f"{path.name} is missing columns: {', '.join(missing)}")

    # Convert types. Anything that cannot be converted becomes NaN/NaT,
    # which the check below turns into a clear error.
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    for column in NUMBER_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    for column in ["date"] + NUMBER_COLUMNS:
        if df[column].isna().any():
            raise DataError(f"Column '{column}' has blank or invalid values.")

    return df
```

- [ ] **Step B.4: Run the tests to verify they pass**

Run: `./venv/Scripts/python -m pytest -v`
Expected: 8 passed.

- [ ] **Step B.5: Load the data in `app.py`**

Replace the whole file with:

```python
"""ShopSmart Sales Dashboard.

Run locally with:  streamlit run app.py
"""

from pathlib import Path

import streamlit as st

import data

DATA_FILE = Path(__file__).parent / "data" / "sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_sales():
    """Load the CSV once and reuse it on every rerun."""
    return data.load_sales(DATA_FILE)


st.title("ShopSmart Sales Dashboard")

# Show a plain-English error instead of a crash if the CSV is unusable.
try:
    sales = get_sales()
except data.DataError as error:
    st.error(str(error))
    st.stop()

st.info("Data loaded. Charts are coming in the next milestones.")
```

- [ ] **Step B.6: Verify the app, including the error path**

Happy path:

```bash
./venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); print('exceptions:', len(at.exception), 'errors:', len(at.error))"
```

Expected: `exceptions: 0 errors: 0`

Error path: temporarily hide the CSV, run the same check, then restore it.

```bash
mv data/sales-data.csv data/sales-data.csv.bak
./venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); print('exceptions:', len(at.exception)); print(at.error[0].value)"
mv data/sales-data.csv.bak data/sales-data.csv
git status --short
```

Expected: `exceptions: 0` and a message starting with `Sales file not found:`. After restoring, `git status --short` must not list `data/sales-data.csv`. If it does, the file was not restored correctly: fix that before continuing.

- [ ] **Step B.7: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-2: Load and validate sales CSV" -m "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step B.8: Milestone check (TASK-2 acceptance criteria)**

- CSV loads with correct types: `test_load_sales_converts_column_types`.
- 482 records, 5 categories, 4 regions: `test_load_sales_reads_real_file_with_expected_shape`.
- Structure validated with a clear error if columns are missing: `test_load_sales_missing_column_is_named_in_error`, plus the error-path check in B.6.

Hand-off: tell the owner TASK-2 is ready to tick, add the `Commit:` hash to, and move to Done.

---

### Plan Task C: KPI cards (milestone: TASK-3)

**Files:**
- Modify: `data.py` (add two functions), `tests/test_data.py` (add fixture and tests), `app.py` (replace the info line with KPI cards)

**Interfaces:**
- Consumes: `data.load_sales`, `sales` and `data.DataError` handling from Plan Task B.
- Produces:
  - `data.total_sales(df) -> float` (sum of `total_amount`)
  - `data.total_orders(df) -> int` (number of distinct `order_id` values)
  - The `sample_sales` pytest fixture in `tests/test_data.py`, reused by Plan Tasks D and E.

- [ ] **Step C.1: Write the failing tests**

Append to `tests/test_data.py`:

```python
# ---- shared sample data for the calculation tests ----


@pytest.fixture
def sample_sales():
    """Four made-up orders with easy-to-check answers.

    Total sales are 480 over two months. Category totals (250, 200, 30) and
    region totals (380, 100) have no ties, so sort order is unambiguous.
    The dates are deliberately not in order.
    """
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2024-02-10", "2024-01-05", "2024-02-11", "2024-01-20"]
            ),
            "order_id": ["ORD-1", "ORD-2", "ORD-3", "ORD-4"],
            "product": ["Smart Watch", "Earbuds", "USB-C Cable", "Speaker"],
            "category": ["Wearables", "Audio", "Accessories", "Audio"],
            "region": ["North", "North", "North", "South"],
            "quantity": [1, 1, 3, 2],
            "unit_price": [200.0, 150.0, 10.0, 50.0],
            "total_amount": [200.0, 150.0, 30.0, 100.0],
        }
    )


# ---- KPIs ----


def test_total_sales(sample_sales):
    assert data.total_sales(sample_sales) == pytest.approx(480.0)


def test_total_orders(sample_sales):
    assert data.total_orders(sample_sales) == 4


def test_real_data_kpis_match_prd():
    df = data.load_sales(REAL_CSV)
    assert data.total_sales(df) == pytest.approx(116500.21, abs=0.01)
    assert data.total_orders(df) == 482
```

- [ ] **Step C.2: Run the tests to verify they fail**

Run: `./venv/Scripts/python -m pytest -v`
Expected: the three new tests FAIL with `AttributeError: module 'data' has no attribute 'total_sales'` (or `total_orders`). The 8 loader tests still pass.

- [ ] **Step C.3: Add the functions to `data.py`**

Append to `data.py`:

```python
def total_sales(df):
    """Total revenue: the sum of every order's total_amount."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Number of distinct orders."""
    return int(df["order_id"].nunique())
```

- [ ] **Step C.4: Run the tests to verify they pass**

Run: `./venv/Scripts/python -m pytest -v`
Expected: 11 passed.

- [ ] **Step C.5: Add the KPI cards to `app.py`**

Replace this line:

```python
st.info("Data loaded. Charts are coming in the next milestones.")
```

with:

```python
# KPI cards: the two headline numbers.
total_sales_col, total_orders_col = st.columns(2)
total_sales_col.metric("Total Sales", f"${data.total_sales(sales):,.0f}")
total_orders_col.metric("Total Orders", f"{data.total_orders(sales):,}")
```

- [ ] **Step C.6: Verify the KPI values in the running app**

```bash
./venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); print('exceptions:', len(at.exception)); print([(m.label, m.value) for m in at.metric])"
```

Expected: `exceptions: 0` and `[('Total Sales', '$116,500'), ('Total Orders', '482')]`.

- [ ] **Step C.7: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-3: Add KPI cards" -m "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step C.8: Milestone check (TASK-3 acceptance criteria)**

- Total Sales shown as currency, about $116,500: C.6 (`$116,500`) and `test_real_data_kpis_match_prd`.
- Total Orders shown with separators, equal to 482: C.6 (`482`) and `test_real_data_kpis_match_prd`.

Hand-off: tell the owner TASK-3 is ready to tick, add the `Commit:` hash to, and move to Done.

---

### Plan Task D: Sales trend chart (milestone: TASK-4)

**Files:**
- Modify: `data.py` (add `monthly_sales`), `tests/test_data.py` (add tests), `app.py` (add import, accent color, trend chart)

**Interfaces:**
- Consumes: `sample_sales` fixture and `REAL_CSV` from `tests/test_data.py`; `sales` from `app.py`.
- Produces:
  - `data.monthly_sales(df) -> pandas.DataFrame` with columns `month` (timestamp of the first day of each month) and `sales` (float), one row per month that has orders, oldest first.
  - In `app.py`: `import plotly.express as px` and the constant `ACCENT`, both reused by Plan Task E.

- [ ] **Step D.1: Write the failing tests**

Append to `tests/test_data.py`:

```python
# ---- monthly trend ----


def test_monthly_sales_one_row_per_month_oldest_first(sample_sales):
    result = data.monthly_sales(sample_sales)
    assert list(result["month"]) == [
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-02-01"),
    ]
    assert list(result["sales"]) == pytest.approx([250.0, 230.0])


def test_real_data_has_twelve_months_that_add_up_to_the_total():
    df = data.load_sales(REAL_CSV)
    result = data.monthly_sales(df)
    assert len(result) == 12
    assert result["sales"].sum() == pytest.approx(data.total_sales(df))
```

- [ ] **Step D.2: Run the tests to verify they fail**

Run: `./venv/Scripts/python -m pytest -v`
Expected: the two new tests FAIL with `AttributeError: module 'data' has no attribute 'monthly_sales'`.

- [ ] **Step D.3: Add `monthly_sales` to `data.py`**

Append to `data.py`:

```python
def monthly_sales(df):
    """Sales per month, oldest first. Columns: month (first day of month), sales."""
    with_month = df.assign(month=df["date"].dt.to_period("M").dt.to_timestamp())
    return (
        with_month.groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
    )
```

- [ ] **Step D.4: Run the tests to verify they pass**

Run: `./venv/Scripts/python -m pytest -v`
Expected: 13 passed.

- [ ] **Step D.5: Add the trend chart to `app.py`**

Add the Plotly import next to the Streamlit import (imports stay alphabetical):

```python
import plotly.express as px
import streamlit as st
```

Add the accent color below `DATA_FILE`:

```python
ACCENT = "#2E6FDB"  # one color for every chart
```

Append at the end of the file:

```python
# Sales trend: one point per month.
monthly = data.monthly_sales(sales)
trend_chart = px.line(
    monthly,
    x="month",
    y="sales",
    markers=True,
    title="Sales Trend by Month",
    labels={"month": "Month", "sales": "Sales ($)"},
)
trend_chart.update_traces(
    line_color=ACCENT,
    hovertemplate="%{x|%b %Y}<br>$%{y:,.2f}<extra></extra>",
)
trend_chart.update_xaxes(tickformat="%b %Y")
trend_chart.update_yaxes(tickprefix="$", tickformat=",")
st.plotly_chart(trend_chart)
```

- [ ] **Step D.6: Verify the chart renders**

```bash
./venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); print('exceptions:', len(at.exception)); print('charts:', len(at.get('plotly_chart')))"
```

Expected: `exceptions: 0` and `charts: 1`. (If `charts` shows 0 even though there are no exceptions, the AppTest lookup name differs in this Streamlit version. Do not guess: report it, and rely on the visual check below.)

- [ ] **Step D.7: Visual check (owner)**

Ask the owner to run `streamlit run app.py` and confirm: a line chart titled "Sales Trend by Month" with 12 monthly points (Jan to Dec 2024), a `$` Y-axis, and hovering a point shows the month and an exact dollar value. Also confirm the terminal shows no warnings. An agent cannot judge appearance, so this step is the owner's.

- [ ] **Step D.8: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-4: Add monthly sales trend chart" -m "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step D.9: Milestone check (TASK-4 acceptance criteria)**

- Line chart by month, time on X and sales on Y: D.5 and D.6.
- Tooltips show exact values, and the chart has clear titles and axis labels: D.5 and the owner's visual check D.7.

Hand-off: tell the owner TASK-4 is ready to tick, add the `Commit:` hash to, and move to Done.

---

### Plan Task E: Category and region breakdowns (milestone: TASK-5)

**Files:**
- Modify: `data.py` (add helper and two functions), `tests/test_data.py` (add tests), `app.py` (add bar charts)

**Interfaces:**
- Consumes: `sample_sales` fixture and `REAL_CSV` from `tests/test_data.py`; `px`, `ACCENT`, `sales` and the trend chart code from `app.py`.
- Produces:
  - `data.sales_by_category(df) -> pandas.DataFrame` with columns `category`, `sales`, sorted highest to lowest.
  - `data.sales_by_region(df) -> pandas.DataFrame` with columns `region`, `sales`, sorted highest to lowest.

- [ ] **Step E.1: Write the failing tests**

Append to `tests/test_data.py`:

```python
# ---- category and region breakdowns ----


def test_sales_by_category_sorted_highest_first(sample_sales):
    result = data.sales_by_category(sample_sales)
    assert list(result["category"]) == ["Audio", "Wearables", "Accessories"]
    assert list(result["sales"]) == pytest.approx([250.0, 200.0, 30.0])


def test_sales_by_region_sorted_highest_first(sample_sales):
    result = data.sales_by_region(sample_sales)
    assert list(result["region"]) == ["North", "South"]
    assert list(result["sales"]) == pytest.approx([380.0, 100.0])


def test_real_data_categories_and_regions():
    df = data.load_sales(REAL_CSV)

    categories = data.sales_by_category(df)
    assert len(categories) == 5
    assert categories["category"].iloc[0] == "Electronics"

    regions = data.sales_by_region(df)
    assert len(regions) == 4
    assert regions["region"].iloc[0] == "North"
```

- [ ] **Step E.2: Run the tests to verify they fail**

Run: `./venv/Scripts/python -m pytest -v`
Expected: the three new tests FAIL with `AttributeError: module 'data' has no attribute 'sales_by_category'` (or `sales_by_region`).

- [ ] **Step E.3: Add the functions to `data.py`**

Append to `data.py`:

```python
def _sales_by(df, column):
    """Total sales for each value of `column`, highest first."""
    return (
        df.groupby(column, as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
        .sort_values("sales", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_category(df):
    """Sales per product category, highest first. Columns: category, sales."""
    return _sales_by(df, "category")


def sales_by_region(df):
    """Sales per region, highest first. Columns: region, sales."""
    return _sales_by(df, "region")
```

- [ ] **Step E.4: Run the tests to verify they pass**

Run: `./venv/Scripts/python -m pytest -v`
Expected: 16 passed.

- [ ] **Step E.5: Add the bar charts to `app.py`**

Append at the end of the file (after the trend chart):

```python
def bar_chart(table, label_column, title):
    """Horizontal bar chart of sales, with the biggest bar on top."""
    chart = px.bar(
        table,
        x="sales",
        y=label_column,
        orientation="h",
        title=title,
        labels={"sales": "Sales ($)", label_column: label_column.title()},
    )
    chart.update_traces(
        marker_color=ACCENT,
        hovertemplate="%{y}<br>$%{x:,.2f}<extra></extra>",
    )
    chart.update_yaxes(categoryorder="total ascending")  # largest bar at the top
    chart.update_xaxes(tickprefix="$", tickformat=",")
    return chart


# Category and region breakdowns, side by side.
category_col, region_col = st.columns(2)
category_col.plotly_chart(
    bar_chart(data.sales_by_category(sales), "category", "Sales by Category")
)
region_col.plotly_chart(
    bar_chart(data.sales_by_region(sales), "region", "Sales by Region")
)
```

The complete `app.py` at the end of this plan task, for reference:

```python
"""ShopSmart Sales Dashboard.

Run locally with:  streamlit run app.py
"""

from pathlib import Path

import plotly.express as px
import streamlit as st

import data

DATA_FILE = Path(__file__).parent / "data" / "sales-data.csv"
ACCENT = "#2E6FDB"  # one color for every chart

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_sales():
    """Load the CSV once and reuse it on every rerun."""
    return data.load_sales(DATA_FILE)


st.title("ShopSmart Sales Dashboard")

# Show a plain-English error instead of a crash if the CSV is unusable.
try:
    sales = get_sales()
except data.DataError as error:
    st.error(str(error))
    st.stop()

# KPI cards: the two headline numbers.
total_sales_col, total_orders_col = st.columns(2)
total_sales_col.metric("Total Sales", f"${data.total_sales(sales):,.0f}")
total_orders_col.metric("Total Orders", f"{data.total_orders(sales):,}")

# Sales trend: one point per month.
monthly = data.monthly_sales(sales)
trend_chart = px.line(
    monthly,
    x="month",
    y="sales",
    markers=True,
    title="Sales Trend by Month",
    labels={"month": "Month", "sales": "Sales ($)"},
)
trend_chart.update_traces(
    line_color=ACCENT,
    hovertemplate="%{x|%b %Y}<br>$%{y:,.2f}<extra></extra>",
)
trend_chart.update_xaxes(tickformat="%b %Y")
trend_chart.update_yaxes(tickprefix="$", tickformat=",")
st.plotly_chart(trend_chart)


def bar_chart(table, label_column, title):
    """Horizontal bar chart of sales, with the biggest bar on top."""
    chart = px.bar(
        table,
        x="sales",
        y=label_column,
        orientation="h",
        title=title,
        labels={"sales": "Sales ($)", label_column: label_column.title()},
    )
    chart.update_traces(
        marker_color=ACCENT,
        hovertemplate="%{y}<br>$%{x:,.2f}<extra></extra>",
    )
    chart.update_yaxes(categoryorder="total ascending")  # largest bar at the top
    chart.update_xaxes(tickprefix="$", tickformat=",")
    return chart


# Category and region breakdowns, side by side.
category_col, region_col = st.columns(2)
category_col.plotly_chart(
    bar_chart(data.sales_by_category(sales), "category", "Sales by Category")
)
region_col.plotly_chart(
    bar_chart(data.sales_by_region(sales), "region", "Sales by Region")
)
```

- [ ] **Step E.6: Verify all three charts render**

```bash
./venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); print('exceptions:', len(at.exception)); print('charts:', len(at.get('plotly_chart')))"
```

Expected: `exceptions: 0` and `charts: 3` (same caveat as D.6 if the lookup returns 0).

- [ ] **Step E.7: Visual check (owner)**

Ask the owner to run `streamlit run app.py` and confirm: the category chart shows 5 bars with Electronics on top and the region chart shows 4 bars with North on top; both sit side by side under the trend chart; tooltips show exact `$` values.

- [ ] **Step E.8: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-5: Add category and region bar charts" -m "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

- [ ] **Step E.9: Milestone check (TASK-5 acceptance criteria)**

- Category chart: 5 categories, sorted highest to lowest, Electronics on top: `test_sales_by_category_sorted_highest_first`, `test_real_data_categories_and_regions`, plus the owner's visual check E.7.
- Region chart: 4 regions, sorted highest to lowest: `test_sales_by_region_sorted_highest_first`, `test_real_data_categories_and_regions`.
- Tooltips with exact values, side-by-side layout under the trend chart: E.5 and the owner's visual check E.7.

Hand-off: tell the owner TASK-5 is ready to tick, add the `Commit:` hash to, and move to Done.

---

### Plan Task F: Testing and refinement (milestone: TASK-6)

**Files:**
- Modify (only if the polish pass finds something): `app.py`, `data.py`, `tests/test_data.py`
- Create (temporary, NOT committed, outside the repo, for example in the scratchpad directory): `cross_check.py`

**Interfaces:**
- Consumes: everything from Plan Tasks A to E.
- Produces: a verified, polished dashboard ready to merge.

- [ ] **Step F.1: Run the full test suite**

Run: `./venv/Scripts/python -m pytest -v`
Expected: 16 passed, no warnings.

- [ ] **Step F.2: Independently cross-check the numbers**

Write a throwaway script `cross_check.py` outside the repo. It recomputes every number with the standard-library `csv` module (no pandas) and compares against `data.py`:

```python
"""One-off check: recompute the dashboard numbers without pandas."""

import collections
import csv
import sys

sys.path.insert(0, ".")  # run from the repo root so `import data` works
import data

rows = list(csv.DictReader(open("data/sales-data.csv", newline="", encoding="utf-8")))
df = data.load_sales("data/sales-data.csv")

assert len(rows) == data.total_orders(df)
assert abs(sum(float(r["total_amount"]) for r in rows) - data.total_sales(df)) < 0.01

for column, function in (
    ("category", data.sales_by_category),
    ("region", data.sales_by_region),
):
    expected = collections.defaultdict(float)
    for r in rows:
        expected[r[column]] += float(r["total_amount"])
    table = function(df)
    got = dict(zip(table[column], table["sales"]))
    assert got.keys() == expected.keys(), column
    for key in expected:
        assert abs(got[key] - expected[key]) < 0.01, (column, key)

by_month = collections.defaultdict(float)
for r in rows:
    by_month[r["date"][:7]] += float(r["total_amount"])
months = data.monthly_sales(df)
assert len(months) == len(by_month)
for month, sales in zip(months["month"], months["sales"]):
    assert abs(by_month[month.strftime("%Y-%m")] - sales) < 0.01

print("cross-check OK")
```

Run it from the repo root: `./venv/Scripts/python <path-to-cross_check.py>`
Expected: `cross-check OK`. Any assertion failure is a real bug in `data.py`: fix it test-first (add a failing test, then the fix) before continuing.

- [ ] **Step F.3: Full app check and load-time check**

```bash
./venv/Scripts/python -c "import time; from streamlit.testing.v1 import AppTest; t = time.time(); at = AppTest.from_file('app.py', default_timeout=30).run(); print('seconds:', round(time.time() - t, 2)); print('exceptions:', len(at.exception), 'errors:', len(at.error)); print([(m.label, m.value) for m in at.metric]); print('charts:', len(at.get('plotly_chart')))"
```

Expected: `seconds` under 5, `exceptions: 0 errors: 0`, metrics `[('Total Sales', '$116,500'), ('Total Orders', '482')]`, `charts: 3`.

- [ ] **Step F.4: Browser and appearance check (owner)**

Ask the owner to run `streamlit run app.py` and check, in at least two of Chrome, Firefox, Edge and Safari: the page loads in under 5 seconds, the layout matches the PRD mockup (KPIs, trend chart, then category and region charts side by side), all labels are clear, and the terminal shows no warnings (including no deprecation warnings). An agent cannot judge this, so it is the owner's step. Record what needs changing, if anything.

- [ ] **Step F.5: Polish pass**

Read `app.py` and `data.py` top to bottom against the Global Constraints. Fix anything that is unclear, missing a short comment, or inconsistent, plus any issue the owner raised in F.4. Keep changes small, and re-run F.1 and F.3 after any edit.

- [ ] **Step F.6: Commit**

If files changed in F.2 or F.5:

```bash
git add -A -- app.py data.py tests/test_data.py
git commit -m "TASK-6: Test and refine dashboard" -m "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
```

If nothing changed, ask the owner whether to record the verification as an empty commit (`git commit --allow-empty -m "TASK-6: Verify dashboard"` plus the trailer) so the milestone has a commit to point to. Do not create it without asking.

- [ ] **Step F.7: Milestone check (TASK-6 acceptance criteria)**

- All values match independent calculations, no errors or warnings: F.1, F.2, F.3.
- Loads in under 5 seconds and looks professional: F.3 (timing) and the owner's check F.4.
- At least two modern browsers checked, code commented and organized: F.4 and F.5.

Hand-off: tell the owner TASK-6 is ready to tick, add the `Commit:` hash to, and move to Done. Then tell them the branch is ready to merge into `main`.

---

### Plan Task G: Deployment to Streamlit Community Cloud (milestone: TASK-7) — OWNER EXECUTES

**This plan task is the owner's to execute. Agents must not perform it.** The owner deploys from `main` after merging `feature/sales-dashboard`. The plan stops here and hands off.

**Before you start:**
- Plan Tasks A to F are committed on `feature/sales-dashboard` and TASK-1 to TASK-6 are done on the board.
- `venv/` is git-ignored, so it is not in the repo. Streamlit Cloud builds its own environment from `requirements.txt`.

- [ ] **Step G.1: Merge to `main` and push (owner)**

Merge `feature/sales-dashboard` into `main` (locally or through a GitHub pull request, whichever you prefer) and push `main` to GitHub. Check that `app.py`, `data.py`, `requirements.txt` and `data/sales-data.csv` are all on `main` on GitHub.

- [ ] **Step G.2: Deploy from `main` (owner)**

At https://share.streamlit.io choose **Create app**, then set the repository to this one, the branch to `main`, and the main file path to `app.py`. Under **Advanced settings**, pick a Python version (the newest offered is fine, since `requirements.txt` uses minimum versions). Click **Deploy**.

If the build fails on a package, read the build log first. The likely cause is a package version that does not exist for the chosen Python version. Choosing a different Python version in the app's settings and rebooting is the first thing to try.

- [ ] **Step G.3: Verify the public URL (owner)**

Open the shareable URL in a private or incognito window (so you are not logged in). Confirm the full dashboard loads without errors: `$116,500` and `482` in the KPI cards, the trend chart, and both bar charts.

- [ ] **Step G.4: Record the result (owner)**

Add the public URL to the project README, commit it with `TASK-7` in the message, then tick the criteria, fill in the `Commit:` line and move TASK-7 to Done in `TASKS.md`.

- [ ] **Step G.5: Milestone check (TASK-7 acceptance criteria)**

- Repository pushed to GitHub and the app deployed on Streamlit Community Cloud: G.1 and G.2.
- The public URL loads the full dashboard without errors, and the link is recorded in the README: G.3 and G.4.

**End of plan.**
