from unittest.mock import MagicMock, patch

from app.ai_reasoner import AIReasoner


def test_ai_reasoner_fallback_without_api_key(monkeypatch):

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    reasoner = AIReasoner()

    result = reasoner.analyze(
        case_name="Test Case",
        evidence=["Unusual IP address"],
        risk_level="MEDIUM",
        confidence=40,
        threat="Credential Attack",
        findings=["Suspicious or unusual IP address detected"]
    )

    assert result["ai_available"] is False
    assert result["ai_summary"] is None
    assert result["ai_reasoning"] is None
    assert result["ai_investigation_steps"] == []


def test_ai_reasoner_success_with_mock(monkeypatch):

    monkeypatch.setenv("GEMINI_API_KEY", "fake-test-key")

    mock_response = MagicMock()
    mock_response.text = """
    {
        "summary": "Credential attack indicators were detected.",
        "reasoning": "Multiple authentication anomalies suggest suspicious credential activity.",
        "investigation_steps": [
            "Review authentication logs",
            "Investigate the source IP"
        ]
    }
    """

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response

    with patch(
        "app.ai_reasoner.genai.Client",
        return_value=mock_client
    ):
        reasoner = AIReasoner()

        result = reasoner.analyze(
            case_name="Credential Case",
            evidence=["Multiple failed login attempts"],
            risk_level="HIGH",
            confidence=90,
            threat="Credential Attack",
            findings=["Multiple failed login attempts detected"]
        )

    assert result["ai_available"] is True
    assert result["ai_summary"] == (
        "Credential attack indicators were detected."
    )
    assert "authentication anomalies" in result["ai_reasoning"]
    assert len(result["ai_investigation_steps"]) == 2


def test_ai_reasoner_fallback_on_api_failure(monkeypatch):

    monkeypatch.setenv("GEMINI_API_KEY", "fake-test-key")

    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = Exception(
        "Simulated Gemini API failure"
    )

    with patch(
        "app.ai_reasoner.genai.Client",
        return_value=mock_client
    ):
        reasoner = AIReasoner()

        result = reasoner.analyze(
            case_name="Failure Case",
            evidence=["Malware detected"],
            risk_level="MEDIUM",
            confidence=40,
            threat="Malware Activity",
            findings=["Potential malware activity detected"]
        )

    assert result["ai_available"] is False
    assert result["ai_summary"] is None
    assert result["ai_reasoning"] is None
    assert result["ai_investigation_steps"] == []
