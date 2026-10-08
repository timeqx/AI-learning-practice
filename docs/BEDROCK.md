# AWS Bedrock implementation labs

Bedrock features and availability vary by region and model. Check the current AWS user guide and console before provisioning; enable only the smallest sandbox resources with budgets and log redaction. **Do not paste access keys into code or Git.**

Official documentation:
- [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Amazon Bedrock Prompt management](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html)
- [Amazon Bedrock Agents](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Amazon Bedrock evaluations](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html)
- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

## Labs: implement and measure, do not just deploy

1. **Knowledge Bases:** upload fictional insurer documents to versioned S3; create KB with supported embedding model/vector index; capture knowledge-base ID, sync job, chunking strategy and ingest status. Test retrieval on tenant/date-separated sources. Do not assume KB filtering alone is sufficient authorization.
2. **Retrieval:** compare your local TF-IDF/BM25, dense retrieval, Bedrock Knowledge Base Retrieve, hybrid (when supported), and reranking. Report Recall@k, MRR, stale-doc rate, latency, and dollars per 1,000 queries.
3. **Guardrails:** write allowed/refused policy matrix with human signoff. Configure content filters, denied topics, sensitive-information handling, contextual grounding where available; test false positives and adversarial misses. Check guardrail invocation on all supported entry points, including direct tool flows.
4. **Prompt Management:** build distinct prompt variants per workflow, publish immutable versions, store a change log, compare candidates on holdout cases and demonstrate rollback.
5. **Agents:** define read-only tool/action schemas for verification and documentation checks. Use explicit approval for any case state mutation. Test retry, timeout, compensation, stale state, and no-permission behavior.
6. **Evaluations:** maintain your independent golden suite; compare to Bedrock evaluation mechanisms and human grading. Version prompts, documents, model IDs, embedding IDs and grader definitions in each result.
7. **Production integration:** use IAM task roles, environment segregation, tracing with sensitive payload exclusion, request budgets, throttling, and audited changes. Conduct threat modeling and data/privacy review before processing anything real.

## Submission per lab

Record architecture diagram, config-as-code (with no secrets), clean-up instructions, example redacted traces, dated model/region details, metric report and residual risks. Run `terraform destroy` or equivalent for disposable resources and verify billable resources are gone.
