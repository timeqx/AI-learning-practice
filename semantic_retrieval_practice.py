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
    allowed = [
        doc for doc in documents
        if doc["tenant"] == tenant
        and doc["workflow"] == workflow
        and date.fromisoformat(doc["effective_from"]) <= as_of
        and (
            doc["effective_until"] is None
            or as_of < date.fromisoformat(doc["effective_until"])
        )
    ]
    
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
            "text": doc["text"]
        })
        
    results.sort(
            key=lambda result: result["score"],
            reverse=True
    )
        
    return results[:top_k]
    

golden_dataset = [
    {
        "question": "How long do I have to send hospital papers?",
        "expected": "CL-OLD"
    },
    {
        "question": "What documents are required for outpatient reimbursement?",
        "expected": "CL-NEW"
    },
    {
        "question": "How can I appeal a rejected insurance claim?",
        "expected": "CL-APPEAL"
    },
    {
        "question": "Impatient insurance claim?",
        "expected": "CL-NEW"
    }
]

def evaluate_retrieval(dataset):
    correct = 0
    
    for case in dataset:
        results = retrieve(
            question=case["question"],
            tenant="demo",
            workflow="claims",
            as_of=date(2026, 6, 1),
            top_k=1
        )
        
        predicted = results[0]["id"] if results else None
        expected = case["expected"]
        
        if predicted == expected:
            correct += 1
            print(f"PASS: {expected}")
        else:
            print(
                f"fail: expected {expected}, "
                f"got {predicted}"
            )
            
    total = len(dataset)
    accuracy = correct / total if total else 0
    
    print(f"\nHit@1: {accuracy:.2%}")
    
    return accuracy


evaluate_retrieval(golden_dataset)