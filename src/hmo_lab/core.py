"""Inspectable lexical baseline; replace with tested RAG in later exercises."""
import hashlib
import json
import re
from datetime import date
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / "data" / "policies.json"
BLOCKED = re.compile(r"ignore previous instructions|reveal the system prompt|developer mode|[\w.+-]+@[\w.-]+\.[a-z]{2,}", re.I)
STOP = {"what", "are", "the", "is", "a", "for", "do", "i", "to", "on", "of", "with", "can", "how"}
def terms(value):
    return set(re.findall(r"[a-z0-9]+", value.lower())) - STOP

def load():
    raw = PATH.read_bytes()
    docs = json.loads(raw)
    assert len({d["id"] for d in docs}) == len(docs), "Duplicate document IDs"
    return docs, hashlib.sha256(raw).hexdigest()[:16]

def assist(workflow, question, tenant="demo", as_of=None):
    if workflow not in {"claims", "enrollment", "endorsements", "billing"}:
        raise ValueError("Unknown workflow")
    if not question.strip():
        raise ValueError("Question must not be empty")
    docs, kb_version = load()
    as_of = as_of or date.today()
    candidates = [d for d in docs if d["tenant"] == tenant and d["workflow"] == workflow
                  and date.fromisoformat(d["effective_from"]) <= as_of
                  and (not d.get("effective_until") or as_of < date.fromisoformat(d["effective_until"]))]
    matches = sorted(
        ((len(terms(question) & terms(d["title"] + " " + d["text"])), d) for d in candidates),
        key=lambda item: (-item[0], item[1]["id"])
    )
    chosen = matches[0][1] if matches and matches[0][0] >= 2 else None
    status = "blocked" if BLOCKED.search(question) else "answered" if chosen else "abstained"
    if status != "answered":
        chosen = None
    result = {
        "status": status,
        "answer": chosen["text"] if chosen else "Unable to answer from authorized evidence. Ask a human reviewer.",
        "citations": [{"id": chosen["id"], "version": chosen["version"]}] if chosen else [],
        "provenance": {"prompt": "extract-v1", "model": "deterministic-baseline-v1",
                       "knowledge_base": kb_version, "guardrail": "pattern-demo-v1"},
        "trace_id": hashlib.sha256(f"{tenant}:{workflow}:{question}:{as_of}".encode()).hexdigest()[:20],
    }
    return result
