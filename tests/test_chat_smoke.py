import pytest


@pytest.mark.asyncio
async def test_ingest_and_chat(client):
    ingest = await client.post(
        "/ingest",
        json={
            "title": "Q1 Compliance",
            "content": "Caregiver training completion reached 92 percent in Q1.",
            "source": "report",
        },
    )
    assert ingest.status_code == 200
    assert ingest.json()["chunks_indexed"] >= 1

    resp = await client.post("/chat", json={"message": "training completion rate"})
    assert resp.status_code == 200
    body = resp.json()
    assert "LLM provider not configured" in body["reply"]
    assert isinstance(body["sources"], list)
