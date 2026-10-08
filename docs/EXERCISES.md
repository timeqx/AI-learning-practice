# Work tickets, interview drills and practical exams

Complete each ticket as if assigned by a Product Lead. **Do not simply ask an agent to implement every step for you**: you must be able to defend every architecture choice during an interview.

## Ticket A — Data ingestion and governance
Fictional insurer changes claim filing deadline from 45 to 30 days on July 1. Store both revisions, block overlapping effective periods, tag tenant/authority, deduplicate by checksum, propagate index update, and add a replay test using two as-of dates. Explain: Why is `updated_at` not the same as `effective_from`? How do you prove the right source was used?

## Ticket B — Retriever design
Build chunkers (fixed tokens, paragraph headings, semantic where appropriate). Implement BM25 and embeddings with metadata filters. Add hybrid retrieval, reranking, MRR and Recall@5. Conduct an ablation with 200 hand-labeled examples. Explain: When does semantic search fail? What is a hard negative? How does chunk overlap affect cost?

## Ticket C — Grounding and prompt library
Use versioned workflow prompts to return JSON. Allow only retrieved source IDs. Implement citation grounding, conflict detection and refusal with no supporting evidence. Record prompt versions and test against the same holdout dataset. Explain: What is prompt drift? Why is an LLM-as-judge not a ground truth label?

## Ticket D — Safe multi-step workflow
Write a read-only claims evidence reviewer. A case may require fetching policy, matching an effective period, checking completeness, and preparing a reviewer note. Tools must use schemas and allowlists, bounded step count, deadlines, idempotency keys, and fail-closed authorization. Explain: Why is agent-generated text not approval authority?

## Ticket E — Adversarial and privacy practice
Plant malicious instructions inside a synthetic insurer PDF/chunk; demonstrate the assistant ignores it. Test untrusted tool output, PII redaction, retrieval cross-tenant requests, citation spoofing, and log leakage. Record exploit attempts and failures without live sensitive data.

## Ticket F — Incident and rollback
A new chunker decreases correct-policy Recall@5. Detect regression, diagnose whether index lag/version filtering/reranker caused it, block release in CI, rollback, create a bug RCA and an added golden test. Re-run historical traces safely.

## Ticket G — AWS comparison
Deploy to Bedrock sandbox with Knowledge Bases, Guardrails, Prompt Management, Agents, and Evaluations. Benchmark identical test cases against your local design. Record which Bedrock services are managed vs which responsibilities remain yours. Explain IAM model invocation rights, tenant protection and logging risks.

## Ticket H — Final take-home exam (timebox yourself)
In 4 hours: given two conflicting policy PDFs with dated revisions and one injected malicious snippet, make a reliable reviewer-assist endpoint, show source citations, no unauthorized tool action, and a pass/fail CI evaluation. Submit a 2-page design review, recorded demo, failure analysis and 10 interview Q&As.

## Study questions (answer in docs/ANSWERS.md)

1. Precision@k vs Recall@k vs MRR vs nDCG?
2. Why can a 100% retrieval score still yield hallucinations?
3. How do you prevent retrieval of documents from another tenant?
4. When do you abstain vs escalate to a specialist?
5. What are effective date, revision date, source authority and KB version?
6. How should reviewer labels be constructed and audited?
7. Why does PII redaction break without realistic adversarial testing?
8. How do you stop prompt injection from retrieved PDFs?
9. What is the difference between detection guardrails and enforcement authorization?
10. How do you replay decisions when models or indexes are no longer available?
11. How do you build a regression gate with stochastic generation?
12. How do you negotiate acceptable safety/accuracy thresholds with Product and Compliance?

## Review rubric (100 points)

Correctness & tests 25; retrieval/evaluation rigor 20; safety and tenant boundaries 20; auditability 15; operational reliability 10; documentation and design tradeoffs 10. Under 80 = rework; any cross-tenant leak or unauthorized action = automatic fail regardless of score.
