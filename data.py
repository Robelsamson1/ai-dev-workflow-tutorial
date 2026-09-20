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


def total_sales(df):
    """Total revenue: the sum of every order's total_amount."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Number of distinct orders."""
    return int(df["order_id"].nunique())


def monthly_sales(df):
    """Sales per month, oldest first. Columns: month (first day of month), sales."""
    with_month = df.assign(month=df["date"].dt.to_period("M").dt.to_timestamp())
    return (
        with_month.groupby("month", as_index=False)["total_amount"]
        .sum()
        .rename(columns={"total_amount": "sales"})
    )

