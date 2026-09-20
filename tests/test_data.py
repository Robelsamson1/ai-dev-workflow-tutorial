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
