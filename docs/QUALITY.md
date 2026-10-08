# Quality framework, scorecard and release gates

## Golden data

Each workflow needs ordinary, edge, outdated-policy, ambiguous, cross-tenant, missing-evidence, adversarial, PII, and multi-document cases. Start from the tiny baseline in data/golden.jsonl, then hand-label at least 50 per workflow and set aside a holdout set. Include source ID/version, authorized tenant, effective date, expected facts, expected refusal/abstention and human-review expectation. Have two reviewers adjudicate disagreements.

## Quantitative measures

Retrieval: Recall@1/5, MRR, nDCG@k, correct active-policy version, retrieval p50/p95.
Generation: factual claim accuracy, citation precision/recall, unsupported-claim rate, schema validity, abstention precision/recall, human escalation correctness.
Security: unauthorized disclosure rate, cross-tenant retrieval rate, PII leakage, injection success rate, tool misuse rate.
Operations: per-model prompt version quality, daily failure slices, exception rate, token cost, p50/p95 latency, provider failures, drift and review backlog.

The local deterministic evaluator checks only **status and citation ID**. It is not an LLM accuracy, faithfulness, or security certification.

## Provisional training gates (negotiate with product/compliance owners)

- Critical tenant or PII disclosure: **zero tolerated in tests**; any confirmed event blocks release and triggers incident response.
- Citation grounding on high-risk workflow: 100% of critical assertions supported in manually reviewed critical slice.
- Workflow-specific answer/citation accuracy: target >= 95% with confidence intervals and representative stratification; increase for regulated consequential cases.
- Schema validity >= 99.9%, measurable retrieval Recall@5 >= 98%, bounded p95 latency/cost against agreed SLO.
- Compare challenger and incumbent on the **same fixed holdout set**. No downgrade in critical cohorts; paired regression failures must be reviewed.

These are illustrative practice thresholds, **not legal or insurer requirements**.

## Regression protocol

1. Pin corpus snapshot, chunker, embedding model/version, vector index, prompt, LLM model, guardrail and tool schemas.
2. Run deterministic tests, retrieval benchmark, full golden suite, adversarial tests, and sampling-based LLM eval with multiple seeds/repeats.
3. Report overall and per-workflow counts, confidence intervals, false refusals, unsafe completions, costs and latency.
4. Label failure cause (retrieval miss, stale document, hallucination, conflicting policy, jailbreak, prompt drift, tool error).
5. Reviewer approves limited staging promotion; use canary and rollback plan. Audit exact deployment version.
6. Never edit gold labels purely to make a failing candidate pass.

## Incident drill

Inject an old inpatient policy into active retrieval. Measure detection lag. Stop promotion, identify impacted traces, assess disclosure/decision impact, revert corpus version, add regression case, publish a postmortem with follow-up owner and deadline.
