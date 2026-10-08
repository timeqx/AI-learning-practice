"""Offline regression harness; run python -m hmo_lab.eval."""
import json
from datetime import date
from pathlib import Path
from .core import assist

DATA = Path(__file__).resolve().parents[2] / "data" / "golden.jsonl"

def evaluate():
    cases = [json.loads(line) for line in DATA.read_text().splitlines() if line.strip()]
    if not cases:
        raise ValueError("Golden set must not be empty")
    failures = []
    for case in cases:
        result = assist(case["workflow"], case["question"], case.get("tenant", "demo"),
                        date.fromisoformat(case["as_of"]))
        citations = [item["id"] for item in result["citations"]]
        if result["status"] != case["status"] or (
            case["status"] == "answered" and case["policy_id"] not in citations
        ) or (case["status"] != "answered" and citations):
            failures.append({"id": case["id"], "actual": result, "expected": case})
    return {"total": len(cases), "pass_rate": (len(cases) - len(failures)) / len(cases),
            "failures": failures}

if __name__ == "__main__":
    report = evaluate()
    print(json.dumps(report, indent=2))
    if report["pass_rate"] < 1:
        raise SystemExit(1)
