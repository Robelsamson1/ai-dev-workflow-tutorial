# ShopSmart Sales Dashboard: Design

Source requirements: `prd/ecommerce-analytics.md`. Milestone tracking: `TASKS.md` (TASK-1 to TASK-7).

## Goal

A single-page Streamlit dashboard that reads `data/sales-data.csv` and shows two KPIs (Total Sales, Total Orders), a monthly sales trend, and sales by category and by region. Phase 1 only: no filters, auth, database or export (PRD Phase 2).

## Decisions made during brainstorming

| Question | Decision |
|----------|----------|
| Trend granularity | Monthly (12 points for 2024) |
| File layout | Two modules: `data.py` (calculations) and `app.py` (layout + Plotly chart code) |
| Bad or missing data | Fail loudly: plain-English error shown with `st.error`, app stops |
| Visual styling | Light touch: wide layout, `st.metric` cards, one accent color, `$` formatting, built-in Streamlit theme |
| Dependency pinning | Minimum versions in `requirements.txt` (e.g. `streamlit>=1.40`) |

## Working rules (from the project owner)

- Work on the current branch `feature/sales-dashboard`. No git worktree.
- Plain Python virtual environment in `venv/` (already git-ignored) with a `requirements.txt`. No uv, no conda.
- Data calculations live in their own module, covered by pytest tests.
- Code stays simple and readable, with comments.
- Deployment (TASK-7) is executed by the owner from `main` after the branch is merged. The implementation plan ends there and hands off.

## Files

```
app.py                 Streamlit page: layout, KPI cards, 3 Plotly charts
data.py                Load and validate the CSV; all calculations (no Streamlit imports)
data/sales-data.csv    Already in the repo
tests/test_data.py     pytest tests for data.py
requirements.txt       streamlit, pandas, plotly, pytest (minimum versions)
venv/                  python -m venv venv (git-ignored)
```

## data.py

Pure functions: a DataFrame goes in, a number or DataFrame comes out. No Streamlit imports, so pytest never needs Streamlit.

| Function | Returns |
|----------|---------|
| `load_sales(path)` | DataFrame with `date` parsed as datetime and numeric columns as numbers. Raises `DataError` on any problem (see below). |
| `total_sales(df)` | Sum of `total_amount` |
| `total_orders(df)` | Number of distinct `order_id` values |
| `monthly_sales(df)` | One row per month (`month`, `sales`), oldest to newest |
| `sales_by_category(df)` | `category`, `sales`, sorted highest to lowest |
| `sales_by_region(df)` | `region`, `sales`, sorted highest to lowest |

`sales_by_category` and `sales_by_region` share one small private helper that groups by a column and sorts.

`DataError` is a small subclass of `ValueError` defined in `data.py`.

## app.py

1. `st.set_page_config` with a title and wide layout.
2. Call `load_sales` (wrapped in `st.cache_data`). On `DataError`: `st.error(str(error))`, then `st.stop()`.
3. Two `st.metric` cards: Total Sales (`$116,500`) and Total Orders (`482`).
4. Full-width line chart of monthly sales.
5. Two columns below it: horizontal bar charts for sales by category and by region, largest bar on top.

All charts use one accent color, clear titles and axis labels, and hover tooltips showing exact `$` values. Chart code is short and stays inline in `app.py`.

## Error handling

`load_sales` raises `DataError` with a plain-English message for each of these cases:

- file not found
- file empty (no rows)
- required columns missing (message names them)
- `date` values that cannot be parsed
- `quantity`, `unit_price` or `total_amount` values that are not numbers

`app.py` is the only place that catches `DataError`. No silent cleaning: a bad file never produces a plausible-looking but wrong dashboard.

## Testing

pytest tests in `tests/test_data.py`, run from the repo root with `pytest`.

- **Calculation tests** use a small hand-built DataFrame where the answers are easy to check by hand: totals, order count, monthly grouping and ordering, and descending sort for category and region.
- **Real-data test** loads `data/sales-data.csv` and checks the PRD's expected values: 482 orders, total sales 116,500.21, Electronics top category, North top region, 5 categories, 4 regions, 12 months.
- **Error tests** write tiny bad CSVs to `tmp_path` and assert `DataError` for: missing file, empty file, missing column, bad date, non-numeric amount.

Charts and layout are verified by running `streamlit run app.py` and checking the page against the PRD's acceptance criteria. There are no automated UI tests.

## Milestone mapping

| Milestone | Delivers |
|-----------|----------|
| TASK-1 | `venv/`, `requirements.txt`, project structure, placeholder `app.py` that runs |
| TASK-2 | `data.py` with `DataError` and `load_sales`, plus its tests |
| TASK-3 | `total_sales`, `total_orders` and the KPI cards |
| TASK-4 | `monthly_sales` and the trend chart |
| TASK-5 | `sales_by_category`, `sales_by_region` and the two bar charts |
| TASK-6 | Full test pass, number cross-check against the CSV, browser and performance checks, polish |
| TASK-7 | Streamlit Community Cloud deployment, executed by the owner from `main` after the merge |

## Out of scope

Everything the PRD lists under Phase 2: authentication, database integration, export, alerts, filtering and date ranges, drill-down, mobile-responsive design.
