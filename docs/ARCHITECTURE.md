# Architecture and production evolution

## Workflow

API -> authenticated tenant context (TODO) -> input safety and PII screening (TODO) -> workflow router -> authorized versioned policy retrieval -> rerank -> context builder -> schema-constrained LLM -> citation/grounding validator -> human decision checkpoint -> privacy-preserving audit -> response.

Current code implements a **transparent keyword matching exercise baseline**, basic policy effective-window filtering, tenant selection, and simplistic prompt-pattern blocking only. It does not yet provide genuine embeddings, RAG generation, identity checks, audit persistence, Bedrock, secure tool execution, or reliable PII protection. Do not serve real HMO traffic.

## Models to introduce

PolicySource(id, insurer, tenant, author, authority, source_url, checksum, updated_at)
PolicyRevision(id, source_id, version, effective_from, effective_until, approval_state)
Chunk(id, revision_id, section, text, embedding_model, embedding_version, token_count)
Case(id, workflow, tenant_id, redacted_question, classification, reviewer_status)
Run(id, trace_id, tenant_id, prompt_version, kb_manifest_sha, model_id, guardrail_id, tool_versions, timestamp)
EvaluationCase(id, expected_behavior, source_revision_ids, difficulty, labeler, split)
HumanReview(id, case_id, suggested_action, reviewer, decision, reason, timestamp)

## Crucial architecture decisions

- **Never trust a tenant ID supplied by the client.** The demo permits one only to illustrate isolation in retrieval; in production derive it from verified identity, perform row-level security and test negative authorization.
- Keep policy ingestion immutable. Validate issuer, version, effective dates and revocations. The same question may have different valid answers in June and October.
- Denials, payments, coverage activation, retroactive endorsement and disclosure of protected information must be performed by a separately authorized human process, **not** free-form model output.
- Never pass secrets, hidden system instructions, or unredacted sensitive data into retriever logs or third-party model calls.
- Store audit event metadata and authorized evidence IDs; protect access to audit records, define retention policy and avoid raw prompts by default.
- Place deterministic policy checks outside the model. Guardrails are defense in depth, not a substitute for authorization or enforcement.
- Test malicious instructions embedded in documents and tool responses, not just malicious user queries.

## Suggested production infrastructure

FastAPI + PostgreSQL (metadata/audit) + S3 versioned policy content + OpenSearch Serverless or pgvector + SQS event ingestion + IAM-limited Bedrock + OpenTelemetry/CloudWatch. All choices require a measured ADR and threat model. Use a synthetic sandbox account, budget alarms, controlled service roles and region-specific service availability.

## Failure injection

Simulate a revoked source, duplicate effective ranges, obsolete embedding index, tenant-crossing retrieval, timeout during a workflow tool call, malicious PDF instructions, schema violation, provider outage, and delayed knowledge-base synchronization. Design fail-closed behavior, alerts, and reviewer escalation.
