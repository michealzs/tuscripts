# Data-Ops Agent Service

A FastAPI + LangChain/LangGraph service that turns the original `tuscripts`
collection of standalone scripts into an API with a retrieval-augmented
data-operations assistant. Each script is ported to a reusable function,
exposed both as an HTTP endpoint and as a LangGraph agent tool.

## Stack

| Concern        | Technology |
|----------------|------------|
| API            | FastAPI + Uvicorn |
| Data           | SQLAlchemy (async) + Postgres (`Document` store) |
| Vector store   | **pgvector** (primary), Weaviate & Pinecone adapters (optional) |
| LLM / agents   | LangChain + LangGraph (`create_react_agent`) |
| Observability  | Langfuse + LangSmith |
| IaC            | Terraform (pgvector container, optional Pinecone index / Weaviate) |

## What was ported

| Original | Now |
|----------|-----|
| `compare_excel_columns.py` (stdin prompts) | `app/domain/excel.py:compare_excel_columns()` + `POST /tools/excel-diff` (file upload) |
| `carecademy.py` (writes CSVs) | `app/domain/careacademy.py:fetch_caregiver_report()` + `POST /tools/careacademy` (returns JSON) |
| `mac_startup.sh` | kept under `scripts/`; setup folded into the `Makefile` |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/healthz`, `/readyz` | Liveness / readiness |
| POST | `/tools/excel-diff` | Diff a column across two uploaded `.xlsx` files |
| POST | `/tools/careacademy` | Fetch + summarise a caregiver-training report |
| POST | `/ingest` | Store a document and embed it into the vector store |
| POST | `/chat` | RAG data-ops assistant (LangGraph) over ingested docs + live tools |

## Run it

```bash
cp .env.example .env          # optionally add DEEPSEEK_API_KEY for full /chat
docker compose up -d --build
curl -X POST localhost:8000/ingest -H 'content-type: application/json' \
     -d '{"title":"Q1","content":"Training completion reached 92% in Q1.","source":"report"}'
curl -X POST localhost:8000/chat -H 'content-type: application/json' \
     -d '{"message":"what was the completion rate?"}'

# excel diff
curl -X POST localhost:8000/tools/excel-diff \
     -F file1=@a.xlsx -F file2=@b.xlsx -F column_name=name
```

Local dev: `make install && make test && make run`.

## Keyless operation

Runs end-to-end with no secrets: the excel-diff and careacademy tools work
directly; embeddings and the vector store fall back to offline implementations,
and `/chat` returns matching document excerpts. Add `DEEPSEEK_API_KEY` (or `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`) for conversational answers and Langfuse/LangSmith keys for
tracing.

## Terraform

```bash
cd terraform && terraform init && terraform plan
terraform apply -var 'enable_pinecone=true'
```
