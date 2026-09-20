# TASKS

This file tracks all work for the ShopSmart Sales Dashboard, based on `prd/ecommerce-analytics.md`. Move each milestone between the To Do, In Progress and Done sections as work progresses.

## Definition of Done

Before any milestone moves to Done, all of the following must be true:

- Every acceptance criterion for the milestone is met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID (e.g. `TASK-3`) in the commit message

## To Do

### TASK-7: Deployment to Streamlit Community Cloud
Publish the dashboard to a public shareable URL for stakeholder review (PRD M7, NFR-5).

- [ ] Repository is pushed to GitHub and the app is deployed on Streamlit Community Cloud
- [ ] The public URL loads the full dashboard without errors, and the link is recorded in the project README

Commit:

## In Progress

## Done

### TASK-1: Environment setup and project initialization
Set up the Python environment, dependencies and project structure for the dashboard (PRD M1).

- [x] Python 3.11+ environment created, with Streamlit, Plotly and Pandas listed in `requirements.txt` and installed
- [x] Project structure in place, including `app.py` and a `data/` folder containing `sales-data.csv`
- [x] `streamlit run app.py` starts and shows a placeholder page without errors

Commit: e659985
Notes: Plan step A.7 still listed the design doc and plan, which were already committed, so only the new files were staged. Otherwise clean.

### TASK-2: Data loading and basic structure
Load and validate `data/sales-data.csv` with Pandas and lay out the modular app structure (PRD M2, FR-5).

- [x] CSV loads with correct types: `date` as a date, numeric columns as numbers, the rest as categories or strings
- [x] The loaded data has 482 records, 5 categories and 4 regions
- [x] The CSV structure is validated before use, with a clear error message if columns are missing (data quality risk)

Commit: 4bba0ff
Notes: clean

### TASK-3: KPI cards
Show Total Sales and Total Orders as prominent KPI cards (PRD M3, FR-1).

- [x] Total Sales is displayed as currency (`$X,XXX,XXX` style) and is about $116,500 for the sample data
- [x] Total Orders is displayed with number separators and equals 482

Commit: a5f2fd7
Notes: clean

### TASK-4: Sales trend chart
Add an interactive line chart of sales over time (PRD M4, FR-2).

- [x] Line chart shows sales by day or month, with time on the X-axis and sales amount on the Y-axis
- [x] Tooltips show exact values, and the chart has clear titles and axis labels

Commit: 54c213d
Notes: clean

### TASK-5: Category and region breakdowns
Add bar charts for sales by product category and by region (PRD M5, FR-3 and FR-4).

- [x] Category bar chart shows all 5 categories, sorted highest to lowest, with Electronics on top
- [x] Region bar chart shows all 4 regions (North, South, East, West), sorted highest to lowest
- [x] Both charts have interactive tooltips with exact values and are laid out side by side below the trend chart

Commit: e07165f
Notes: clean

### TASK-6: Testing and refinement
Verify the numbers, polish the appearance and check performance and browser compatibility (PRD M6).

- [x] All displayed values match independent calculations from the CSV, and the app runs with no errors or warnings
- [x] Dashboard loads in under 5 seconds and looks professional enough for an executive presentation (clear labels, consistent styling)
- [x] Checked in at least two modern browsers (e.g. Chrome and Firefox), with code commented and cleanly organized

Commit: 6312632
Notes: clean
