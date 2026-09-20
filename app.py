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
