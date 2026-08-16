from app.analyzer import Analyzer
from app.models import InvestigationResult
from app.utils import normalize_text
from app.ai_reasoner import AIReasoner


class InvestigationEngine:

    def __init__(self):
        self.analyzer = Analyzer()
        self.ai_reasoner = AIReasoner()

    def investigate(self, case_name, evidence):

        score, findings = self.analyzer.analyze(evidence)

        evidence_text = normalize_text(" ".join(evidence))

        if (
            "failed login" in evidence_text
            or "brute force" in evidence_text
            or "unusual ip" in evidence_text
        ):
            threat = "Credential Attack"
            hypothesis = (
                "Possible credential compromise or brute-force activity "
                "originating from a suspicious source."
            )

        elif (
            "malware" in evidence_text
            or "malicious process" in evidence_text
        ):
            threat = "Malware Activity"
            hypothesis = (
                "Potential malicious software execution requiring "
                "endpoint investigation and containment."
            )

        elif (
            "network" in evidence_text
            or "outbound connection" in evidence_text
        ):
            threat = "Network Anomaly"
            hypothesis = (
                "Potentially suspicious network communication requiring "
                "traffic and endpoint analysis."
            )

        else:
            threat = "Suspicious Activity"
            hypothesis = (
                "Observed activity contains anomalies that require "
                "additional investigation."
            )

        if score >= 70:
            risk = "HIGH"

            recommendations = [
                "Immediately review relevant security logs",
                "Investigate the source of the suspicious activity",
                "Reset affected credentials if compromise is suspected",
                "Monitor affected systems for additional indicators"
            ]

        elif score >= 40:
            risk = "MEDIUM"

            recommendations = [
                "Review relevant security logs",
                "Verify the user's recent activity",
                "Investigate the suspicious indicator",
                "Continue monitoring for additional anomalies"
            ]

        else:
            risk = "LOW"

            recommendations = [
                "Continue monitoring",
                "Review the event if additional evidence appears"
            ]

        ai_result = self.ai_reasoner.analyze(
            case_name=case_name,
            evidence=evidence,
            risk_level=risk,
            confidence=score,
            threat=threat,
            findings=findings
        )

        return InvestigationResult(
            case_name=case_name,
            risk_level=risk,
            confidence=score,
            threat=threat,
            attack_hypothesis=hypothesis,
            findings=findings,
            recommendations=recommendations,
            **ai_result
        )
