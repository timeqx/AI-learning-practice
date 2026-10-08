# One capstone: HMO Operations AI Quality Platform

Build one progressively hardened AI assistant for a **fictional** health maintenance organization. Workflows: claims, enrollment, endorsements, billing. Synthetic data only, with explicit human approval before consequential actions. You will implement the project yourself; do not skip exercises by copying reference answers.

## Outcomes

Demonstrate Python services, RAG architecture, source governance, embeddings, retrieval and reranking, prompt engineering, bounded agents, evaluations, PII handling, attack testing, audit traces, quality monitoring, incident response, and AWS Bedrock. A working demo does not substitute for 2+ years of production experience: keep an evidence portfolio of incidents, load tests, reviews, and deployments.

## 12 milestones (suggested 12–20 weeks)

| Sprint | Learn | Implement | Definition of done |
|---|---|---|---|
| 01 | Python typing, packaging, FastAPI, pytest, Pydantic, dependency injection | Typed API, domain models, tests, lint, CI | Validated schemas, unit/integration tests, trace IDs |
| 02 | Insurance vocabulary, policy periods, source authority | Synthetic policy ingestion + metadata, active versions, immutable source hashes | Reject duplicates, expired docs, tenant mixing |
| 03 | Chunking, TF-IDF/BM25, embeddings | Reproducible retrieval baseline with document/chunk IDs | Recall@k, MRR, stratified 50+ queries |
| 04 | Vector indexes, hybrid search, rerankers | Compare lexical/vector/hybrid and reranking with held-out queries | Ablation report and latency/cost tradeoffs |
| 05 | Context windows, conflicting evidence, citation grounding | Token-budget assembly; citation validator; abstention | No unsupported claims in critical eval slice |
| 06 | Structured prompting, model tradeoffs | Versioned prompts and provider adapters; JSON schema validation | Prompt registry + eval gate for every change |
| 07 | Multi-step agents, tools, state, idempotency | Enrollment checker and claims evidence reviewer (read-only); typed tools | Finite steps, retries, timeout, approval checkpoint |
| 08 | Threat modeling, PHI/PII, access control | Prompt injection suites, redaction, authN/authZ, tenant filtering | Demonstrable cross-tenant denial and attack report |
| 09 | Dataset design, labeling agreement, eval statistics | Golden sets, adversarial cases, paired regression tests, human review queue | Thresholds agreed per workflow; CI blocks regressions |
| 10 | AWS IAM, Bedrock Knowledge Bases, Guardrails, Prompt Management, Evaluations, Agents | Optional sandbox AWS implementation with least-privilege roles | Side-by-side local vs Bedrock report with version logs |
| 11 | SRE, monitoring, releases, observability | Metrics, dashboards, drift alarms, rollback, incident playbook | Simulated regression and postmortem; replayable audit |
| 12 | System design and hiring evidence | Deploy secured staging, perform load/cost tests, record architecture decisions | Demo, design review, risk register, scorecards, runbook |

## Every sprint is a real work simulation

1. Read linked official docs; explain unfamiliar terms in your own words.
2. Write a mini-design: requirements, failure modes, metrics, security assumptions.
3. Create a test proving a missing capability fails; implement the smallest correct fix.
4. Compare before/after quality and cost with repeatable commands.
5. Open a PR with screenshots/logs, dataset version, decision trace, tradeoffs, and reviewer questions.
6. Produce an incident or quality note; do not silently adjust golden labels to make tests pass.

## Completion levels

- Level 1: tests and golden set green with synthetic rules baseline.
- Level 2: RAG with source/version governance and calibrated abstention.
- Level 3: controlled tool-using workflows and adversarial eval.
- Level 4: operational monitoring, human review, audit replay, secured Bedrock staging.
- Level 5: independent architecture critique, production-style incident response and benchmark evidence.

## Evidence to publish

Create `portfolio/` with architecture diagram, ADRs, PR writeups, retrieval ablations, model/prompt comparison, threat model, eval dashboard, incident postmortem, cloud cost notes, and a 10-minute demo. Sanitize all examples. Do not publish live credentials or medical data.

Start at [EXERCISES.md](EXERCISES.md), and use [QUALITY.md](QUALITY.md) for release gates.
