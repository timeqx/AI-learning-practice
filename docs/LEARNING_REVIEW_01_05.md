# Reviewer — AI Engineering Lessons 1–5

> Companion [Notion learning dashboard](https://app.notion.com/p/3f42ada7252c81599529da51093165ce) · [Detailed flashcard reviewer](https://app.notion.com/p/3f42ada7252c8153bc8ce07a55c9088a)
> Practise with **synthetic HMO documents only**. This is a learner's reference, not an insurer decision system.

## 1. Mental model

RAG = **Retrieval-Augmented Generation**. The intended workflow: verified identity / tenant + question -> active-policy filtering -> relevant document retrieval -> context assembly -> model answer -> grounding/citation validation -> human review for consequential decisions. Our current `hmo_lab` starter performs deterministic policy lookup, and the scripts implement embedding retrieval. **No language model currently generates policy answers in the practice scripts.**

| Term | In plain English | In our repo |
| --- | --- | --- |
| Knowledge base | Collection of documents the system may consult | `data/policies.json` and temporary in-memory examples |
| Retrieval | Choose relevant source material | `retrieve(...)` |
| Embedding | Learned numeric vector of text | `SentenceTransformer.encode()` |
| Similarity | Compare how aligned vectors are | `question_vector @ document_vector` |
| Grounding | Tie claims to authorized evidence | Citation IDs, validation to be built |
| Evaluation | Compare result against independently verified expectations | Golden dataset, Hit@1 |
| Reranking | Reorder candidate documents with a stronger scorer | Future milestone |
| Guardrails | Policies and runtime checks restricting model behavior | Future milestone (not a substitute for authorization) |

## 2. Python and FastAPI review

- `print(value)` writes to terminal; `return value` makes it available to caller. A function without explicit `return` returns `None`.
- `documents, version = load()` unpacks a tuple; `next(...)` finds the first match; dictionaries use `doc["id"]`; `documents.extend([...])` changes only the in-memory list.
- `zip(docs, vectors)` pairs document and embedding; `enumerate(results, start=1)` produces human-readable rankings.
- FastAPI `@app.post("/assist")` registers a route. **404** can mean wrong path, app or port; **422** is commonly schema validation failure.
- The existing server is a development demo; a caller-provided tenant string is NOT authorization.

## 3. Keyword retrieval

`terms(text)` generates normalized token sets. `query_terms & document_terms` intersects them; `len(...)` produces a simple overlap score. Exact overlaps miss semantically equivalent expressions (“send hospital papers” versus “file inpatient claim”). Stop word filtering can accidentally remove meaning (especially negation); treat set overlap as a teaching baseline, not industry-grade retrieval.

## 4. Embeddings + semantic retrieval

`sentence-transformers/all-MiniLM-L6-v2` produces 384-dimensional embeddings. `model.encode(texts, normalize_embeddings=True)` creates unit vectors; `query_vector @ document_vector` is the dot product and equals cosine similarity for normalized vectors. A larger cosine score generally signals semantic similarity, **not** probability of a correct claim decision.

Filter eligible documents by correct workflow, authorized tenant and policy effective window **before** ranking. The sample filters `effective_from <= as_of` and `as_of < effective_until` when an end exists; `None` means open-ended. Real authorization must be enforced using verified identity rather than an untrusted request parameter.

`top_k=1` returns at most one ranked document; `top_k=3` returns at most three. The highest score can still point to an irrelevant document, so high quality retrieval also needs negative tests and abstention strategies. The exercise recomputes document embeddings every request; future work should persist/reuse versioned vectors.

## 5. Golden datasets and evaluation

A **golden case** specifies an input, independently reviewed expected policy ID(s), tenant, workflow and **its own effective date**. Never change a label simply to turn a failure green.

- **Hit@1**: expected document at rank one, averaged over test cases.
- **Hit@K**: a relevant document anywhere in top K.
- **Recall@K**: fraction of all relevant documents retrieved in top K.
- **MRR**: average reciprocal rank of the first relevant document (rank 1 -> 1, rank 2 -> 0.5).

Three passing test questions yield 100% Hit@1 **only on those cases**. They do not establish safety, accurate generated answers or production reliability.

### Observed experiment (June 2026)

| Query topic | Expected first policy | Observed cosine score |
| --- | --- | --- |
| Hospital papers submission | CL-OLD | 0.475 |
| Outpatient reimbursement requirements | CL-OUT | 0.759 |
| Appeal rejected claim | CL-APPEAL | 0.760 |

### Fix the current evaluator in `semantic_retrieval_practice.py`

1. Outpatient case wrongly expects `CL-NEW`; the correct expectation is `CL-OUT`.
2. All cases use hardcoded `as_of=date(2026,6,1)` even the October case. Give each case an `as_of` ISO date and pass `date.fromisoformat(case["as_of"])`.
3. Replace accidental “Impatient” typo with an unambiguous inpatient question first; then add typo cases as robustness tests.
4. Add an empty-result case and a wrong-tenant case. Avoid interpreting a missing document as an embedding failure.
5. Keep deterministic fixture data and expected versions controlled. Add per-case failure output, not just an aggregate pass percentage.

## 6. Flashcard questions

1. Difference between `print` and `return`?
2. Why does set intersection miss semantically equivalent wording?
3. What does `normalize_embeddings=True` do? Why does `@` calculate cosine then?
4. Why can a score of 0.9 still be wrong?
5. What is `top_k` and why does it matter for context size?
6. Explain why `CL-OLD` is valid in June 2026 and `CL-NEW` in October 2026.
7. What is Hit@1? What is a golden dataset?
8. What happens when the relevant document isn't in the corpus?
9. Why is taking `tenant` directly from client input insecure?
10. Why should document embeddings be indexed rather than recomputed every question?

**Mastery check:** Explain all ten questions in your own words, intentionally break a retrieval case, find why it failed, fix it and provide a reproducible test result.

Next: repair the evaluator, implement Hit@K / Recall@K / MRR, then compare lexical and semantic retrieval with real golden sets.

[Curriculum](ROADMAP.md) · [Practice tickets](EXERCISES.md) · [Evaluation standards](QUALITY.md)
