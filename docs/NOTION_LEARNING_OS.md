# Notion Learning OS — HMO AI Quality Lab

> This is the companion *management workspace* for [AI-learning-practice](https://github.com/timeqx/AI-learning-practice). Code, evaluations, and versioned technical specifications live in GitHub. Notion is the learning/product management hub. **Notion does not automatically sync with GitHub.**

## Workspace

- [Dashboard](https://app.notion.com/p/3f43acc62d0d81428a84cc85aa117f26)
- [Reviewer](https://app.notion.com/p/3f43acc62d0d8137a67dcc961b3ae4c6)
- [Learning Roadmap](https://app.notion.com/p/cf90ed0b0f3348d283ca2f2d5f9e5afa)
- [Practice Backlog](https://app.notion.com/p/7ed66791777141d3b62c5ee8bf7c2bd2)
- [Knowledge & Flashcards](https://app.notion.com/p/2afc9f1779214eb982c3cf4daf4cfcb2)
- [Evaluation Experiments](https://app.notion.com/p/f252d743a6044e1581185607c8193dc9)
- [Learning Sessions](https://app.notion.com/p/aa6d6217dd3149e88124e83039b07fef)
- [Operating Guide](https://app.notion.com/p/3f43acc62d0d8143ab0cebf7f902f1d7)
- [Product Blueprint](https://app.notion.com/p/3f43acc62d0d819cb13cc1c119267b78)

## Organized section pages

The Notion home is now a clean overview. Each domain has its own page, database, and views:

- [01 · Roadmap & Progress](https://app.notion.com/p/3f43acc62d0d81c9a31de916620555da) — milestone status chart, evidence and mastery.
- [02 · Practice & Sprint Board](https://app.notion.com/p/3f43acc62d0d81268603f136ee772e4e) — priority queue and Kanban.
- [03 · Study Notes & Flashcards](https://app.notion.com/p/3f43acc62d0d81a28fbfdea4b9a2484f) — reviewer, concept cards and review calendar.
- [04 · Evaluation & Quality Metrics](https://app.notion.com/p/3f43acc62d0d81db86d5dd2175d00fd8) — golden evaluation results and cosine comparison chart.
- [05 · Learning Sessions & Journal](https://app.notion.com/p/3f43acc62d0d815081d9e8caa30ead01) — study journal and calendar.
- [06 · Product Architecture & Guides](https://app.notion.com/p/3f43acc62d0d81e8abadf1ba80eb1e78) — capstone blueprint and usage guide.

All original Notion data entries were preserved during reorganization. The home retains a collapsed group of older linked views; the working views are located on their corresponding section pages.

## Visual lessons and AI pipelines

The knowledge and architecture sections now contain independent diagram-first pages (native Notion Mermaid diagrams, examples, terminology, and practice links). Existing reviewer, databases, experiment records, and progress trackers are preserved.

### Topic-based lesson notes

- [Lesson 01: Python, FastAPI & RAG big picture](https://app.notion.com/p/3f43acc62d0d81349b76c408d623efe9)
- [Lesson 02: Keyword search & lexical matching](https://app.notion.com/p/3f43acc62d0d81e29f33fc711d934b47)
- [Lesson 03: Embeddings & cosine similarity](https://app.notion.com/p/3f43acc62d0d81c28720ddd6c96b6162)
- [Lesson 04: Authorized semantic retrieval](https://app.notion.com/p/3f43acc62d0d81168203fe0f6500cd2e)
- [Lesson 05: Golden sets & retrieval metrics](https://app.notion.com/p/3f43acc62d0d81549938c8b49abba3ab)
- [Visual AI glossary: terms, connections, diagrams](https://app.notion.com/p/3f43acc62d0d817e9458cf7fe2830b2c)

### System pipelines

- [Pipeline A: Query-time RAG](https://app.notion.com/p/3f43acc62d0d813b8a3ffbe647761ed8)
- [Pipeline B: Policy ingestion & vector indexing](https://app.notion.com/p/3f43acc62d0d81039864d44c2ee256e1)
- [Pipeline C: Evaluation & safety gates](https://app.notion.com/p/3f43acc62d0d810d9ef4e030ee72e1c7)

Use GitHub for source-controlled exercises and technical specifications. Notion is a learning tracker and interactive reference, not a live GitHub sync.

## Workflows

1. **Choose:** select an active ticket in the Notion Practice Backlog.
2. **Understand:** read reviewer and answer flashcard in your own words.
3. **Build:** write and test a small change in the GitHub project.
4. **Fail deliberately:** test an edge case, wrong data, a stale policy or tenant mismatch.
5. **Measure:** report independently labeled retrieval metrics or quality checks (don't fabricate them).
6. **Record:** attach actual command results, GitHub commit/PR URL and notes to the task.
7. **Review:** grade your confidence and revisit weak topics.

## Current known test defects

In `semantic_retrieval_practice.py` as of the review on 2026-10-09:
- The outpatient question expects `CL-NEW`, although `CL-OUT` is the relevant synthetic policy.
- The evaluator uses `as_of=date(2026, 6, 1)` for all cases, including a case expecting `CL-NEW`, which becomes effective July 1, 2026.

The Notion task board tracks these as unresolved until tested fixes are committed. Do not treat reported cosine scores or three manual matches as an independently validated production baseline.

## HMO project boundaries

Use synthetic-only claims/insurer records. The Python starter is a local educational baseline, not a production-safe claims approval or medical decision service. The future roadmap includes provenance, human review, security, AWS Bedrock, evaluations, and incident response.

## Maintaining alignment

When you change a ticket status or lesson in Notion, update its evidence link and test results. When you add new guided code exercises or accepted technical designs, commit them to GitHub, then reference them in Notion. No automation or two-way synchronization has been configured.
