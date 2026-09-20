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
