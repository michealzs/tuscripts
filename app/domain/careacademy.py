"""CareAcademy caregiver-training report.

Ported from the original ``carecademy.py``. Instead of writing CSV files it
returns structured JSON, and the agency id / credentials are parameters rather
than hard-coded. The scrape targets the same ``administrator_dashboard_vue_config``
payload; it is best-effort (the upstream markup may change) and returns an empty
report rather than raising.
"""
from __future__ import annotations

import json
import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    )
}


def fetch_caregiver_report(
    agency_id: int,
    username: str,
    password: str,
    timeout: int = 20,
) -> dict:
    url = f"https://go.careacademy.com/api/agencies/{agency_id}/"
    caregivers: list[dict] = []
    try:
        page = requests.get(
            url, auth=(username, password), headers=HEADERS, timeout=timeout
        )
        soup = BeautifulSoup(page.text, "html.parser")
        script = soup.find("script", attrs={"id": "administrator_dashboard_vue_config"})
        if script and script.string:
            data = json.loads(str(script.string))
            caregivers = data.get("caregiver_list", []) or []
    except Exception as exc:
        logger.warning("CareAcademy fetch failed for agency %s: %s", agency_id, exc)

    return summarize_caregivers(caregivers)


def summarize_caregivers(caregivers: list[dict]) -> dict:
    """Apply the original completion logic to a caregiver list."""
    completed: list[dict] = []
    uncompleted: list[dict] = []
    for c in caregivers:
        done = c.get("initial_completed", 0)
        total = c.get("total_initial", 0)
        status = "Training Completed" if done >= total else "Training Not Completed"
        record = {
            "name": f"{c.get('last_name', '').strip()} {c.get('first_name', '').strip()}".strip(),
            "phone_number": c.get("phone_number"),
            "completed": done,
            "total": total,
            "status": status,
        }
        (completed if status == "Training Completed" else uncompleted).append(record)

    return {
        "total": len(caregivers),
        "completed_count": len(completed),
        "uncompleted_count": len(uncompleted),
        "completed": completed,
        "uncompleted": uncompleted,
    }
