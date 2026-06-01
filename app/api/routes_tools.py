"""Endpoints wrapping the ported scripts."""
from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.domain.careacademy import fetch_caregiver_report
from app.domain.excel import compare_excel_columns
from app.domain.schemas import CareAcademyRequest, ExcelDiffResponse

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/excel-diff", response_model=ExcelDiffResponse)
async def excel_diff(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    column_name: str = Form("value"),
    column_index: int = Form(1),
):
    """Compare a column across two uploaded .xlsx files (ported excel script)."""
    try:
        result = compare_excel_columns(
            await file1.read(),
            await file2.read(),
            column_name=column_name,
            column_index=column_index,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"could not parse spreadsheets: {exc}")
    return result


@router.post("/careacademy")
async def careacademy(payload: CareAcademyRequest):
    """Fetch + summarise a CareAcademy caregiver-training report (ported)."""
    report = fetch_caregiver_report(
        payload.agency_id, payload.username, payload.password
    )
    return report
