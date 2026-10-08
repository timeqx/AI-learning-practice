"""Local development only: unauthenticated; never expose to the internet."""
from datetime import date
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field
from .core import assist

app = FastAPI(title="Synthetic HMO AI Quality Lab")
class Request(BaseModel):
    workflow: Literal["claims", "enrollment", "endorsements", "billing"]
    question: str = Field(min_length=1, max_length=1500)
    tenant: str = Field(default="demo", min_length=1)
    as_of: date | None = None

@app.get("/health")
def health():
    return {"status": "ok", "environment": "synthetic-local"}

@app.post("/assist")
def query(request: Request):
    return assist(request.workflow, request.question, request.tenant, request.as_of)
