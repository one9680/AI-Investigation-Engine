from app.utils import normalize_text


class Analyzer:

    def analyze(self, evidence):

        score = 0
        findings = []

        unique_evidence = list(dict.fromkeys(
            normalize_text(item)
            for item in evidence
            if item.strip()
        ))

        for text in unique_evidence:

            # Authentication failure indicators
            if any(term in text for term in [
                "failed login",
                "login failure",
                "authentication failure",
                "authentication failures",
                "failed authentication"
            ]):
                score += 30
                findings.append(
                    "Multiple failed login or authentication attempts detected"
                )

            # Suspicious IP indicators
            if any(term in text for term in [
                "unusual ip",
                "unknown ip",
                "unrecognized ip",
                "unrecognised ip",
                "new ip",
                "suspicious ip"
            ]):
                score += 40
                findings.append(
                    "Suspicious or unusual IP address detected"
                )

            # After-hours indicators
            if any(term in text for term in [
                "midnight",
                "after hours",
                "outside business hours",
                "outside normal hours",
                "late night",
                "overnight"
            ]):
                score += 20
                findings.append(
                    "Login occurred outside normal hours"
                )

            # Brute-force indicators
            if any(term in text for term in [
                "brute force",
                "password guessing",
                "credential stuffing"
            ]):
                score += 50
                findings.append(
                    "Possible brute-force or credential attack detected"
                )

            # Malware indicators
            if any(term in text for term in [
                "malware",
                "malicious software",
                "malicious executable"
            ]):
                score += 40
                findings.append(
                    "Potential malware activity detected"
                )

            # Malicious process indicators
            if any(term in text for term in [
                "malicious process",
                "suspicious process",
                "unauthorized process"
            ]):
                score += 30
                findings.append(
                    "Suspicious malicious process detected"
                )

            # Outbound network indicators
            if any(term in text for term in [
                "outbound connection",
                "outbound network connection",
                "outbound traffic",
                "external connection"
            ]):
                score += 30
                findings.append(
                    "Unusual outbound network connection detected"
                )

            # Large transfer / exfiltration indicators
            if any(term in text for term in [
                "large volume",
                "large amount",
                "large data",
                "data exfiltration",
                "high volume transfer",
                "large transfer"
            ]):
                score += 30
                findings.append(
                    "Abnormally large data transfer detected"
                )

            # Unknown external destination indicators
            if any(term in text for term in [
                "unknown external host",
                "unrecognized external host",
                "unrecognised external host",
                "unknown external server",
                "suspicious remote host"
            ]):
                score += 30
                findings.append(
                    "Connection to unknown external host detected"
                )

        return min(score, 100), findings
