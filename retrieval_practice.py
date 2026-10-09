from hmo_lab.core import load, terms
from sentence_transformers import SentenceTransformer

documents, version = load()

policy = next(
    doc for doc in documents
    if doc["id"] == "CL-NEW"
)

questions = [
    "inpatient claim filing deadline",
    "How long do i have to send the hospital papers?",
    "What is the weather on Mars?"
]

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

policy_text = policy["title"] + " " + policy["text"]

texts = [policy_text] + questions

embeddings = model.encode(
    texts,
    normalize_embeddings=True
)

policy_vector = embeddings[0]

for index, question in enumerate(questions):
    keyword_score = len(
        terms(question) & terms(policy_text)
    )
    
    question_vector = embeddings[index + 1]
    
    semantic_score = float(
        question_vector @ policy_vector
    )
    
    print(f"\nQuestion: {question}")
    print(f"Keyword score: {keyword_score}")
    print(f"Semantic similiraty: {semantic_score:.3f}")