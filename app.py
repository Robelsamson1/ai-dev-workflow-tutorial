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

# KPI cards: the two headline numbers.
total_sales_col, total_orders_col = st.columns(2)
total_sales_col.metric("Total Sales", f"${data.total_sales(sales):,.0f}")
total_orders_col.metric("Total Orders", f"{data.total_orders(sales):,}")
