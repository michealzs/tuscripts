"""LangChain tools for the data-ops assistant."""
from __future__ import annotations

import json

from app.config import get_settings
from app.domain.careacademy import fetch_caregiver_report
from app.vectorstores import get_vector_store


def search_documents_raw(query: str, k: int = 4) -> list[dict]:
    store = get_vector_store(get_settings())
    return [
        {"text": d.text, "metadata": d.metadata, "score": d.score}
        for d in store.similarity_search(query, k=k)
    ]


def build_tools() -> list:
    from langchain_core.tools import tool

    @tool
    def search_documents(query: str) -> str:
        """Search previously ingested documents/reports for relevant context."""
        return json.dumps(search_documents_raw(query))

    @tool
    def careacademy_report(agency_id: int, username: str, password: str) -> str:
        """Fetch and summarise a CareAcademy caregiver-training completion report."""
        return json.dumps(fetch_caregiver_report(agency_id, username, password))

    return [search_documents, careacademy_report]
