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

        category_scores = {
            "Credential Attack": 0,
            "Malware Activity": 0,
            "Network Anomaly": 0,
        }

        evidence_text = " ".join(evidence).lower().replace("-", " ").replace("_", " ")

        from app.analyzer import INDICATOR_RULES

        for category, weight, terms in INDICATOR_RULES:
            if any(term in evidence_text for term in terms):
                category_scores[category] += weight

        evidence_text = normalize_text(" ".join(evidence))

        if max(category_scores.values()) > 0:
            threat = max(category_scores, key=category_scores.get)
        else:
            threat = "Suspicious Activity"

        hypotheses = {
            "Credential Attack": (
                "Possible credential compromise or brute-force activity "
                "originating from a suspicious source."
            ),
            "Malware Activity": (
                "Potential malicious software execution requiring "
                "endpoint investigation and containment."
            ),
            "Network Anomaly": (
                "Potentially suspicious network communication requiring "
                "traffic and endpoint analysis."
            ),
            "Suspicious Activity": (
                "Observed activity contains anomalies that require "
                "additional investigation."
            ),
        }

        hypothesis = hypotheses[threat]

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

