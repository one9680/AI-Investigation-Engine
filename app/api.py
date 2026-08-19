from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from app.engine import InvestigationEngine


app = FastAPI(
    title="AI Investigation Engine",
    description="Cybersecurity investigation and threat analysis prototype",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvestigationRequest(BaseModel):
    case_name: str
    evidence: List[str]


engine = InvestigationEngine()


@app.get("/")
def root():
    return {
        "message": "AI Investigation Engine API",
        "status": "online",
        "version": "2.0.0"
    }


@app.post("/investigate")
def investigate(request: InvestigationRequest):

    result = engine.investigate(
        request.case_name,
        request.evidence
    )

    return result.model_dump()
