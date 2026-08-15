from pydantic import BaseModel
from typing import List


class InvestigationCase(BaseModel):
    case_name: str
    description: str
    evidence: List[str]


class InvestigationResult(BaseModel):
    case_name: str
    risk_level: str
    confidence: int
    threat: str
    attack_hypothesis: str
    findings: List[str]
    recommendations: List[str]
