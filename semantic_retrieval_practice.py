from datetime import date
from hmo_lab.core import load
from sentence_transformers import SentenceTransformer

documents, version = load()

documents.extend([
    {
        "id": "CL-OUT",
        "tenant": "demo",
        "workflow": "claims",
        "title": "Outpatient claim requirements",
        "text": "Outpatient reimbursement requires an official receipt and physician request.",
        "version": "1",
        "effective_from": "2026-01-01",
        "effective_until": None,
    },
    {
        "id": "CL-APPEAL",
        "tenant": "demo",
        "workflow": "claims",
        "title": "Claim appeal procedure",
        "text": "Members can appeal a denied insurance claim by requesting human review.",
        "version": "1",
        "effective_from": "2026-01-01",
        "effective_until": None,
    },
])

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def retrieve(question, tenant, workflow, as_of, top_k=3):
    allowed = []
    
    for doc in documents:
        if doc["tenant"] != tenant:
            continue
        
        if doc["workflow"] != workflow:
            continue
        start = date.fromisoformat(doc["effective_from"])
        end = doc["effective_until"]

        if as_of < start:
            continue

        if end is not None and as_of >= date.fromisoformat(end):
            continue
        
        allowed.append(doc)
    
    if not allowed:
        return []
    
    texts = [
        doc["title"] + ". " + doc["text"]
        for doc in allowed
    ]
    
    document_vectors = model.encode(
        texts,
        normalize_embeddings=True
    )
    
    query_vector = model.encode(
        question,
        normalize_embeddings=True
    )
    
    results = []
    
    for doc, vector in zip(allowed, document_vectors):
        score = float(query_vector @ vector)
        
        results.append({
            "id": doc["id"],
            "title": doc["title"],
            "score": score,
            "text": doc["text"],
        })
        
    results.sort(
            key=lambda result: result["score"],
            reverse=True
    )
        
    return results[:top_k]
    

golden_dataset = [
    {
    "question": "What is the inpatient claim filing deadline?",
    "expected_ids": ["CL-NEW"],
    "tenant": "demo",
    "workflow": "claims",
    "as_of": date(2026, 10, 8)
    },
    {
        "question": "How long do I have to send hospital papers?",
        "expected_ids": ["CL-OLD"],
        "tenant": "demo",
        "workflow": "claims",
        "as_of": date(2026, 6, 1)
    },
    {
        "question": "What documents are required for outpatient reimbursement?",
        "expected_ids": ["CL-OUT"],
        "tenant": "demo",
        "workflow": "claims",
        "as_of": date(2026, 10, 8)
    },
    {
        "question": "How can I appeal a rejected insurance claim?",
        "expected": [],
        "tenant": "222",
        "workflow": "claims",
        "as_of": date(2026, 10, 8)
    },
        {
        "question": "What documents are required for outpatient reimbursement and how can I appeal a rejected claim?",
        "expected_ids": ["CL-OUT", "CL-APPEAL"],
        "tenant": "demo",
        "workflow": "claims",
        "as_of": date(2026, 10, 8)
    },
    {
        "question": "How can I appeal a rejected insurance claim?",
        "expected_ids": [],
        "tenant": "222",
        "workflow": "claims",
        "as_of": date(2026, 10, 8)
    }
]

def evaluate_retrieval(dataset):
    
    k_values = [1, 2, 3]
    hit_totals = {k: 0 for k in k_values}
    recall_totals = {k: 0.0 for k in k_values}
    
    reciprocal_rank_total = 0.0
    answerable_count = 0
    negative_passes = 0
    negative_count = 0
    
    for case in dataset:

        results = retrieve(
            question=case["question"],
            tenant=case["tenant"],
            workflow=case["workflow"],
            as_of=case["as_of"],
            top_k=max(k_values)
        )
        
        ranked_ids = [result["id"] for result in results]
        relevant_ids = set(case["expected_ids"])
        
        print(f"\nQUESTION: {case['question']}")
        print(f"EXPECTED: {list(relevant_ids)}")
        print(f"RETRIEVED: {ranked_ids}")
        
        if not relevant_ids:
            negative_count += 1
            
            if not ranked_ids:
                negative_passes += 1
                print("PASS: No document returned")
            else:
                print("FAIL: Unexpected documents returned")
                
            continue
       
        answerable_count += 1
        
        for k in k_values:
            top_ids = set(ranked_ids[:k])
            found = top_ids & relevant_ids
            
            hit = int(bool(found))
            recall = len(found) / len(relevant_ids)
            
            hit_totals[k] += hit
            recall_totals[k] += recall
            
            print(
                f"K={k} | Hit={hit} | Recall={recall:.2%}"
            )
        
        first_rank = next(
            (
                rank
                for rank, doc_id in enumerate(ranked_ids, start=1)
                if doc_id in relevant_ids
            ),
            None
        )
        
        reciprocal_rank = 1 / first_rank if first_rank else 0
        reciprocal_rank_total += reciprocal_rank
            
        print(f"Reciprocal Rank: {reciprocal_rank:.3f}")
        
        print("\n--- FINAL EVALUATION ---")
        
    for k in k_values:
        hit_at_k = hit_totals[k] / answerable_count if answerable_count else 0
        recall_at_k = recall_totals[k] / answerable_count if answerable_count else 0
        
        print(f"Hit@{k}: {hit_at_k:.2%}")
        print(f"Recall@{k}: {recall_at_k:.2%}")
        
    mrr = (
        reciprocal_rank_total / answerable_count
        if answerable_count else 0
    )
    
    print(f"MRR: {mrr:.3f}")
    print(f"Negative Tests passed: {negative_passes/negative_count}")

evaluate_retrieval(golden_dataset)