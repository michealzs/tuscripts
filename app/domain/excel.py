"""Excel column comparison.

Ported from the original ``compare_excel_columns.py``. The interactive stdin
prompts are replaced with a pure function that operates on file bytes, so it
can be driven from an API endpoint or an agent tool.
"""
from __future__ import annotations

import io

import pandas as pd


def compare_excel_columns(
    file1: bytes,
    file2: bytes,
    column_name: str = "value",
    sheet1: str | int = 0,
    sheet2: str | int = 0,
    column_index: int = 1,
) -> dict:
    """Return rows present in only one of the two files' target column.

    Mirrors the original logic: read one column from each sheet, then keep the
    rows that do not appear in both (symmetric difference via drop_duplicates).
    """
    df1 = pd.read_excel(
        io.BytesIO(file1), sheet_name=sheet1, usecols=[column_index], names=[column_name]
    )
    df2 = pd.read_excel(
        io.BytesIO(file2), sheet_name=sheet2, usecols=[column_index], names=[column_name]
    )
    differences = pd.concat([df1, df2]).drop_duplicates(keep=False)
    values = differences[column_name].astype(str).tolist()
    return {
        "column": column_name,
        "file1_rows": int(len(df1)),
        "file2_rows": int(len(df2)),
        "difference_count": len(values),
        "differences": values,
    }
