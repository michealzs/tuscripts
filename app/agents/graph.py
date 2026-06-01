"""LangGraph ReAct agent for the data-ops assistant.

Real LangGraph agent when an LLM provider is configured; a deterministic
document-search fallback otherwise, so /chat works and tests pass offline.
"""
from __future__ import annotations

from app.config import Settings, get_settings
from app.observability import configure_langsmith, get_callbacks

SYSTEM_PROMPT = (
    "You are a data-operations assistant. Use search_documents to ground answers "
    "in ingested reports and careacademy_report to pull live caregiver-training "
    "data when asked. Be precise and cite the document or figures you used."
)


class DataOpsAgent:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._graph = None
        if self.settings.llm_configured:
            try:
                self._graph = self._build_graph()
            except Exception:  # pragma: no cover
                self._graph = None

    def _build_graph(self):
        from langgraph.prebuilt import create_react_agent

        from app.agents.tools import build_tools

        configure_langsmith(self.settings)
        return create_react_agent(self._llm(), build_tools())

    def _llm(self):
        if self.settings.llm_provider == "anthropic":
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model=self.settings.chat_model,
                api_key=self.settings.anthropic_api_key,
            )
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=self.settings.chat_model, api_key=self.settings.openai_api_key
        )

    def run(self, message: str) -> dict:
        if self._graph is None:
            return self._fallback(message)
        result = self._graph.invoke(
            {"messages": [("system", SYSTEM_PROMPT), ("user", message)]},
            config={"callbacks": get_callbacks(self.settings)},
        )
        messages = result.get("messages", [])
        reply = messages[-1].content if messages else ""
        used = [
            m.name
            for m in messages
            if getattr(m, "type", "") == "tool" and getattr(m, "name", None)
        ]
        return {"reply": reply, "used_tools": sorted(set(used)), "sources": []}

    def _fallback(self, message: str) -> dict:
        from app.agents.tools import search_documents_raw

        hits = search_documents_raw(message, k=4)
        sources = [str(h["metadata"].get("document_id", "")) for h in hits]
        lines = [
            "LLM provider not configured — returning matching document excerpts. "
            "Set OPENAI_API_KEY (or ANTHROPIC_API_KEY) for full answers."
        ]
        if hits:
            for h in hits:
                lines.append(f"- ({h['metadata'].get('title', 'doc')}) {h['text'][:200]}")
        else:
            lines.append("No documents ingested yet — POST /ingest first.")
        return {
            "reply": "\n".join(lines),
            "used_tools": ["search_documents"] if hits else [],
            "sources": sources,
        }


_agent: DataOpsAgent | None = None


def get_agent() -> DataOpsAgent:
    global _agent
    if _agent is None:
        _agent = DataOpsAgent()
    return _agent


def reset_agent() -> None:
    global _agent
    _agent = None
