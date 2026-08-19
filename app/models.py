from pydantic import BaseModel, Field
from typing import List, Optional


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

    ai_available: bool = False
    ai_summary: Optional[str] = None
    ai_reasoning: Optional[str] = None
    ai_investigation_steps: List[str] = Field(default_factory=list)
