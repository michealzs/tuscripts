"""Ingest documents into the DB + vector store for Q&A."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.domain.models import Document
from app.domain.schemas import DocumentIn, IngestResponse
from app.vectorstores import get_vector_store

router = APIRouter(prefix="/ingest", tags=["ingest"])


def _chunk(text: str, size: int = 500) -> list[str]:
    words = text.split()
    return [" ".join(words[i : i + size]) for i in range(0, len(words), size)] or [text]


@router.post("", response_model=IngestResponse)
async def ingest_document(payload: DocumentIn, session: AsyncSession = Depends(get_session)):
    doc = Document(content=payload.content, title=payload.title, source=payload.source)
    session.add(doc)
    await session.commit()
    await session.refresh(doc)

    chunks = _chunk(payload.content)
    metadatas = [
        {"document_id": doc.id, "title": doc.title, "source": doc.source, "chunk": i}
        for i in range(len(chunks))
    ]
    get_vector_store().add_texts(texts=chunks, metadatas=metadatas)
    return IngestResponse(document_id=doc.id, chunks_indexed=len(chunks))
