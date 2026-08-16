import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()


class AIAnalysis(BaseModel):
    summary: str = Field(
        description="Concise cybersecurity analyst summary of the investigation."
    )
    reasoning: str = Field(
        description="Explain how the supplied evidence relates to the detected threat."
    )
    investigation_steps: List[str] = Field(
        description="Recommended next investigation steps for a security analyst."
    )


class AIReasoner:
    """
    Optional Gemini reasoning layer.

    Risk score and risk level remain controlled by the deterministic
    investigation engine. Gemini only provides contextual reasoning,
    correlation, and analyst-oriented investigation guidance.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite"
        )

    def is_available(self) -> bool:
        return bool(self.api_key)

    def fallback(self) -> Dict[str, Any]:
        return {
            "ai_available": False,
            "ai_summary": None,
            "ai_reasoning": None,
            "ai_investigation_steps": []
        }

    def analyze(
        self,
        case_name: str,
        evidence: List[str],
        risk_level: str,
        confidence: int,
        threat: str,
        findings: List[str]
    ) -> Dict[str, Any]:

        if not self.is_available():
            return self.fallback()

        prompt = f"""
You are assisting a cybersecurity analyst.

Analyze the investigation context below.

IMPORTANT RULES:
- Do not change or recalculate the supplied risk level.
- Do not change or recalculate the supplied numerical score.
- Treat the rule-based findings as objective detections.
- Explain relationships between the evidence.
- Do not claim that remediation actions were actually performed.
- Recommend investigation steps only.
- Keep the response concise and suitable for a SOC analyst.

Case name:
{case_name}

Evidence:
{evidence}

Deterministic risk level:
{risk_level}

Deterministic rule score:
{confidence}

Threat classification:
{threat}

Rule-based findings:
{findings}
"""

        try:
            client = genai.Client(api_key=self.api_key)

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": AIAnalysis,
                    "temperature": 0.2
                }
            )

            analysis = AIAnalysis.model_validate_json(response.text)

            return {
                "ai_available": True,
                "ai_summary": analysis.summary,
                "ai_reasoning": analysis.reasoning,
                "ai_investigation_steps": analysis.investigation_steps
            }

        except Exception:
            return self.fallback()
