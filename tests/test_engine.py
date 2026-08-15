from app.engine import InvestigationEngine


def test_high_risk_investigation():

    engine = InvestigationEngine()

    evidence = [
        "Multiple failed login attempts",
        "Unusual IP address",
        "Login occurred at midnight"
    ]

    result = engine.investigate(
        "Test Case",
        evidence
    )

    assert result.risk_level == "HIGH"
    assert result.confidence == 90
    assert result.threat == "Credential Attack"
    assert len(result.findings) == 3


def test_low_risk_investigation():

    engine = InvestigationEngine()

    evidence = [
        "Normal successful login"
    ]

    result = engine.investigate(
        "Normal Login",
        evidence
    )

    assert result.risk_level == "LOW"
    assert result.confidence == 0
    assert result.threat == "Suspicious Activity"


def test_medium_risk_investigation():

    engine = InvestigationEngine()

    evidence = [
        "Unusual IP address"
    ]

    result = engine.investigate(
        "Medium Risk Case",
        evidence
    )

    assert result.risk_level == "MEDIUM"
    assert result.confidence == 40
    assert result.threat == "Credential Attack"
