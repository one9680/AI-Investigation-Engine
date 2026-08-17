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

def test_duplicate_evidence_does_not_inflate_score():

    engine = InvestigationEngine()

    evidence = [
        "Unusual IP address",
        "Unusual IP address",
        "Unusual IP address"
    ]

    result = engine.investigate(
        "Duplicate Evidence Case",
        evidence
    )

    assert result.risk_level == "MEDIUM"
    assert result.confidence == 40
    assert len(result.findings) == 1

def test_hyphenated_brute_force_is_detected():

    engine = InvestigationEngine()

    evidence = [
        "Repeated brute-force authentication attempts detected"
    ]

    result = engine.investigate(
        "Brute Force Case",
        evidence
    )

    assert result.risk_level == "MEDIUM"
    assert result.confidence == 50
    assert result.threat == "Credential Attack"
    assert "Possible brute-force or credential attack detected" in result.findings


def test_natural_language_credential_attack():

    engine = InvestigationEngine()

    evidence = [
        "Multiple authentication failures were recorded",
        "Access originated from an unrecognized IP address",
        "The account was accessed after hours"
    ]

    result = engine.investigate(
        "Supervisor Custom Investigation",
        evidence
    )

    assert result.risk_level == "HIGH"
    assert result.confidence == 90
    assert result.threat == "Credential Attack"
    assert len(result.findings) == 3
