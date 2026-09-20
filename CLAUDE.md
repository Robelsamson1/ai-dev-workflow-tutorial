# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A tutorial on an AI-assisted dev workflow (PRD → `TASKS.md` → Superpowers brainstorming/plans → code → deploy), with a working project built along the way: the ShopSmart sales dashboard, a single-page Streamlit app over `data/sales-data.csv` (482 orders, 2024). The top-level `*.md` files (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`, `codex-companion.md`, `capstone-tools.md`) are tutorial prose for students, not project docs. Requirements live in `prd/ecommerce-analytics.md`; the design and implementation plan are in `docs/superpowers/specs/` and `docs/superpowers/plans/`.

## Commands

Use the plain `venv/` (git-ignored) and call its Python directly. There is no activation step, and it works in both PowerShell and Git Bash. No uv or conda.

```bash
python -m venv venv && ./venv/Scripts/python -m pip install -r requirements.txt   # one-time setup
./venv/Scripts/python -m pytest -v                                                # all tests
./venv/Scripts/python -m pytest tests/test_data.py::test_total_sales -v           # single test
./venv/Scripts/python -m streamlit run app.py --server.headless true              # run the app
```

- Pass `--server.headless true` when launching from an agent or any non-interactive shell. Without it, first-run Streamlit prompts for an onboarding email on stdin and exits.
- `pytest.ini` sets `pythonpath = .` and `testpaths = tests`, so tests can `import data` from the repo root.
- No linter or formatter is configured.
- Headless app check without a browser (returns exception/error counts, metrics and chart count):
  `./venv/Scripts/python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py', default_timeout=30).run(); print(len(at.exception), len(at.error), [(m.label, m.value) for m in at.metric], len(at.get('plotly_chart')))"`
  A `missing ScriptRunContext` warning from this is expected and harmless. Visual and browser checks can't be automated and are done by the owner.

## Architecture

Two modules, deliberately:

- `data.py` holds pure pandas functions and no Streamlit imports: `load_sales`, `total_sales`, `total_orders`, `monthly_sales`, `sales_by_category`, `sales_by_region`. Every calculation lives here and is covered by `tests/test_data.py`.
- `app.py` is a thin page: cached `get_sales()`, two `st.metric` KPI cards, and three Plotly charts (trend line, then category and region bars side by side). Chart code stays inline, and the shared `ACCENT` color and `bar_chart()` helper are defined there.

Error contract: `load_sales` raises `data.DataError` (a `ValueError` subclass) with a plain-English message for a missing file, an empty file, missing columns, unparseable dates or non-numeric amounts. `app.py` is the only place that catches it (`st.error` + `st.stop()`). Never silently clean bad data.

Tests use a hand-built `sample_sales` fixture (answers checkable by hand, no ties in sort order) plus real-data tests pinned to the PRD's numbers: 482 orders, $116,500.21 total, Electronics top category, North top region, 12 months.

## Workflow conventions

- Work happens on `feature/sales-dashboard`. Don't create worktrees or other branches unless asked.
- Two ID schemes: `TASKS.md` milestones are **TASK-1..TASK-7**, while plan tasks are lettered **A..G** with steps like `F.2`. The plan maps letters to milestones.
- Every commit message starts with the milestone ID (e.g. `TASK-3: Add KPI cards`) and ends with the `Co-Authored-By` trailer given in the session's attribution instructions.
- `TASKS.md` is the owner's board. Move a milestone or tick criteria, fill in `Commit:` and add `Notes:` only when asked. Milestone commits and board-update commits are separate.
- TASK-7 (Streamlit Community Cloud deployment) is executed by the owner from `main` after the branch merges. Agents stop before it and don't merge into `main` unless told to.
- Keep code simple and short-commented so the owner can follow it. Dependencies use minimum versions in `requirements.txt`.

## Lessons

Drawn from the `Notes:` lines in `TASKS.md`. TASK-2 to TASK-6 all finished `clean`, so only TASK-1 produced a lesson.

- Plan steps can be stale. A plan's `git add` list may name files that are already committed (TASK-1's step A.7 did). Check `git status` before staging, stage only what is actually new or changed, and record the deviation in the milestone's `Notes:` line.
