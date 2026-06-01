import io

import pandas as pd
import pytest

from app.domain.careacademy import summarize_caregivers


def _xlsx(values: list[str]) -> bytes:
    """Build an .xlsx with a label column + a value column (index 1)."""
    df = pd.DataFrame({"label": list(range(len(values))), "value": values})
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()


@pytest.mark.asyncio
async def test_excel_diff(client):
    file1 = _xlsx(["alice", "bob", "carol"])
    file2 = _xlsx(["alice", "bob", "dave"])
    resp = await client.post(
        "/tools/excel-diff",
        files={
            "file1": ("a.xlsx", file1, "application/vnd.ms-excel"),
            "file2": ("b.xlsx", file2, "application/vnd.ms-excel"),
        },
        data={"column_name": "name"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert set(body["differences"]) == {"carol", "dave"}
    assert body["difference_count"] == 2


def test_summarize_caregivers():
    caregivers = [
        {"first_name": "A", "last_name": "One", "initial_completed": 3, "total_initial": 3},
        {"first_name": "B", "last_name": "Two", "initial_completed": 1, "total_initial": 3},
    ]
    report = summarize_caregivers(caregivers)
    assert report["completed_count"] == 1
    assert report["uncompleted_count"] == 1
