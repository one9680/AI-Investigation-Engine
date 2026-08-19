from app.engine import InvestigationEngine


def main():

    print("=" * 60)
    print("        AI INVESTIGATION ENGINE")
    print("=" * 60)

    case_name = "Suspicious Login Investigation"

    evidence = [
        "Multiple failed login attempts detected",
        "Login originated from an unusual IP address",
        "Login occurred at midnight"
    ]

    engine = InvestigationEngine()

    result = engine.investigate(
        case_name,
        evidence
    )

    print(f"\nCase: {result.case_name}")
    print(f"Risk Level: {result.risk_level}")
    print(f"Risk Score: {result.confidence}/100")

    print("\nFindings:")

    for finding in result.findings:
        print(f"  [+] {finding}")

    print("\nRecommended Actions:")

    for recommendation in result.recommendations:
        print(f"  -> {recommendation}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
