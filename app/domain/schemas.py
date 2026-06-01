"""Pydantic schemas for the data-ops API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ExcelDiffResponse(BaseModel):
    column: str
    file1_rows: int
    file2_rows: int
    difference_count: int
    differences: list[str]


class CareAcademyRequest(BaseModel):
    agency_id: int
    username: str
    password: str


class DocumentIn(BaseModel):
    content: str
    title: str = ""
    source: str = "manual"


class IngestResponse(BaseModel):
    document_id: int
    chunks_indexed: int


class ChatRequest(BaseModel):
    message: str = Field(..., examples=["What did the last report say about completion rates?"])
    session_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    used_tools: list[str] = []
    sources: list[str] = []
