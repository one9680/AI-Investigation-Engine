class Analyzer:

    def analyze(self, evidence):

        score = 0
        findings = []

        for item in evidence:

            text = item.lower()

            # Authentication threats
            if "failed login" in text:
                score += 30
                findings.append(
                    "Multiple failed login attempts detected"
                )

            if "unusual ip" in text:
                score += 40
                findings.append(
                    "Suspicious or unusual IP address detected"
                )

            if "midnight" in text or "after hours" in text:
                score += 20
                findings.append(
                    "Login occurred outside normal hours"
                )

            if "brute force" in text:
                score += 50
                findings.append(
                    "Possible brute-force attack detected"
                )

            # Malware / endpoint threats
            if "malware" in text:
                score += 40
                findings.append(
                    "Potential malware activity detected"
                )

            if "malicious process" in text:
                score += 30
                findings.append(
                    "Suspicious malicious process detected"
                )

            # Network threats
            if (
                "outbound connection" in text
                or "outbound network connection" in text
            ):
                score += 30
                findings.append(
                    "Unusual outbound network connection detected"
                )

            if (
                "large volume" in text
                or "large amount" in text
                or "large data" in text
            ):
                score += 30
                findings.append(
                    "Abnormally large data transfer detected"
                )

            if "unknown external host" in text:
                score += 30
                findings.append(
                    "Connection to unknown external host detected"
                )

        return min(score, 100), findings
