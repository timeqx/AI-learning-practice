# HMO AI Quality Engineering Lab

One continuous, hands-on project designed around a real-world **AI Engineer (HMO operations)** job description. Build an AI quality function supporting claims, enrollment, endorsements, and billing using **synthetic data only**.

The included Python/FastAPI program is a deliberately simple **deterministic baseline** — it is NOT an LLM, robust RAG implementation, secure production app, or automated insurance decision system. In subsequent practice tickets, you implement embeddings, hybrid retrieval, reranking, AWS Bedrock, prompt management, guardrails, agent tools, evaluation dashboards, and audit infrastructure.

## Start

Requires Python 3.11 or later.

```bash
git clone https://github.com/timeqx/AI-learning-practice.git
cd AI-learning-practice
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest -q
python -m hmo_lab.eval
uvicorn hmo_lab.api:app --reload
```

POST to http://127.0.0.1:8000/assist:

```json
{"workflow":"claims","question":"inpatient claim filing deadline","tenant":"demo","as_of":"2026-10-08"}
```

Access API docs at http://127.0.0.1:8000/docs. Never use actual patient or insurer information. This dev API lacks authentication and must not be exposed publicly.

## Learning material

- [12-milestone guided curriculum](docs/ROADMAP.md)
- [Production architecture and missing components](docs/ARCHITECTURE.md)
- [Hands-on implementation tickets and interview exams](docs/EXERCISES.md)
- [Accuracy benchmarks, evaluations, release gates](docs/QUALITY.md)
- [AWS Bedrock Knowledge Bases, Guardrails, Agents, Prompts and Evaluations labs](docs/BEDROCK.md)
- [Versioned prompt specification](prompts/extract-v1.md)

## Your goal

By the end you should have reproducible tests and benchmarks, dated policies, multi-tenant authorization, versioned prompts and knowledge bases, prompt-injection tests, defensible human approval workflows, AWS sandbox experiments, operational dashboards, incident runbooks, and a public evidence portfolio. This is training and can strengthen a portfolio; it does not confer years of production employment experience.

## Learning management dashboard (Notion)

Track your lessons, practical tickets, review cards, evaluation scores and study sessions in the [AI Engineering OS](https://app.notion.com/p/3f43acc62d0d81428a84cc85aa117f26). The workspace is a companion to this repository, not an automatic two-way sync.

- [Lesson 1–5 Reviewer](https://app.notion.com/p/3f43acc62d0d8137a67dcc961b3ae4c6)
- [Notion workspace & learning workflow guide](docs/NOTION_LEARNING_OS.md)
