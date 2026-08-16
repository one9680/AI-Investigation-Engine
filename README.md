# AI Investigation Engine

A cybersecurity investigation prototype that analyzes security evidence, detects suspicious indicators, calculates an explainable risk score, classifies likely threats, generates an attack hypothesis, and recommends analyst response actions.

The current version uses a **deterministic rule-based investigation engine**. The architecture is intentionally designed so that an **LLM reasoning layer can be added later without replacing the explainable security scoring logic**.

## Project Overview

Security analysts often need to review multiple indicators before deciding whether an activity is benign, suspicious, or potentially malicious.

The AI Investigation Engine demonstrates how security evidence can be processed through a structured investigation workflow:

```text
User Evidence
     ↓
Web Dashboard
     ↓
FastAPI Backend
     ↓
Investigation Engine
     ↓
Rule-Based Analyzer
     ↓
Risk Scoring
     ↓
Threat Classification
     ↓
Attack Hypothesis
     ↓
Findings & Recommendations
     ↓
Investigation Report
```

The project focuses on:

* Explainable security analysis
* Deterministic risk scoring
* Threat classification
* Analyst-friendly findings
* Investigation recommendations
* Modular architecture
* API-based frontend/backend separation
* Testability
* Future AI/LLM integration

## Problem Statement

Security investigations involve correlating multiple pieces of evidence such as failed logins, suspicious IP addresses, malware activity, unusual network connections, and abnormal data transfers.

Manually assessing these indicators can be time-consuming and inconsistent.

This project provides a prototype investigation engine that transforms raw security evidence into a structured investigation result containing:

* Risk level
* Confidence score
* Threat classification
* Attack hypothesis
* Detected findings
* Recommended response actions

## Objectives

The main objectives of the project are to:

1. Accept cybersecurity evidence from a user.
2. Detect known suspicious indicators.
3. Calculate an explainable numerical risk score.
4. Determine a LOW, MEDIUM, or HIGH risk level.
5. Classify the likely type of security threat.
6. Generate an attack hypothesis.
7. Produce investigation findings.
8. Recommend analyst response actions.
9. Display the results through a web dashboard.
10. Maintain a modular architecture for future AI reasoning integration.

## Features

### Rule-Based Security Analysis

The analyzer checks evidence against predefined security indicators such as:

* Failed login attempts
* Unusual IP addresses
* After-hours authentication
* Brute-force activity
* Malware detection
* Malicious processes
* Suspicious outbound connections
* Large data transfers
* Unknown external hosts

Each indicator contributes to an explainable security score.

### Risk Scoring

The total score is capped at 100.

Current risk thresholds:

```text
70–100  → HIGH
40–69   → MEDIUM
0–39    → LOW
```

### Threat Classification

The engine currently identifies broad threat categories:

* Credential Attack
* Malware Activity
* Network Anomaly
* Suspicious Activity

### Attack Hypothesis

Based on the detected threat category, the system generates a concise hypothesis describing the likely security situation.

### Investigation Findings

Matched security indicators are converted into analyst-friendly findings.

### Recommended Response

The system provides recommended investigation or response actions based on the risk level.

The prototype **does not automatically perform remediation** such as blocking IP addresses, resetting passwords, or terminating processes.

### Web Dashboard

The frontend provides:

* New investigation form
* Predefined demo scenarios
* Risk level
* Confidence score
* Threat class
* Attack hypothesis
* Findings
* Recommended actions
* Investigation history
* Report export

### Investigation History

Completed investigations are stored temporarily in browser memory during the current session.

This is prototype-level history and is not currently backed by a database.

### Report Export

Investigation results can be exported as a text report containing:

* Case details
* Risk level
* Confidence
* Threat class
* Attack hypothesis
* Findings
* Recommended response

## Architecture

The current architecture is:

```text
                    USER
                      |
                      v
              WEB DASHBOARD
                      |
                      v
                  FASTAPI
                      |
                      v
            INVESTIGATION ENGINE
                      |
             +--------+--------+
             |                 |
             v                 v
          ANALYZER       THREAT LOGIC
             |                 |
             +--------+--------+
                      |
                      v
              INVESTIGATION RESULT
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
      Risk        Findings      Response
      Score                       Actions
```

## Future Hybrid AI Architecture

The project is designed to evolve into a hybrid cybersecurity investigation system:

```text
                    USER
                      |
                      v
              WEB DASHBOARD
                      |
                      v
                  FASTAPI
                      |
                      v
            INVESTIGATION ENGINE
                      |
             +--------+--------+
             |                 |
             v                 v
       RULE ANALYZER       AI REASONER
             |                 |
       Objective data      LLM reasoning
             |                 |
             +--------+--------+
                      |
                      v
               SYNTHESIS LAYER
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
        Risk       Findings    Hypothesis
        Score                   + Reasoning
                      |
                      v
               FINAL REPORT
```

The deterministic rule engine will remain responsible for explainable scoring.

A future LLM reasoning layer can provide:

* Evidence correlation
* Contextual reasoning
* Analyst-style explanations
* Improved attack hypotheses
* Investigation priorities
* Natural-language summaries
* Suggested next investigation steps

The application should continue functioning even if the LLM service is unavailable.

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### Frontend

* HTML
* CSS
* JavaScript

### Testing

* pytest

### Configuration

* python-dotenv

### Version Control

* Git
* GitHub

## Project Structure

```text
AI-Investigation-Engine/
│
├── app/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── api.py
│   ├── engine.py
│   └── models.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_engine.py
│
├── data/
│   └── cases/
│
├── web/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

The `.env` file is excluded from Git and must never contain publicly committed API keys or secrets.

## Installation

Clone the repository:

```bash
git clone https://github.com/one9680/AI-Investigation-Engine.git
cd AI-Investigation-Engine
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI backend:

```powershell
python -m uvicorn app.api:app --reload
```

The backend normally runs at:

```text
http://127.0.0.1:8000
```

Open the frontend:

```powershell
start web\index.html
```

## API

### Health Endpoint

```http
GET /
```

Used to confirm that the backend is online.

### Investigation Endpoint

```http
POST /investigate
```

Example request:

```json
{
  "case_name": "Credential Compromise Investigation",
  "evidence": [
    "Multiple failed login attempts detected",
    "Login originated from an unusual IP address",
    "Login occurred at midnight"
  ]
}
```

Example investigation output includes:

* Case name
* Risk level
* Confidence
* Threat class
* Attack hypothesis
* Findings
* Recommendations

## Demo Scenarios

### Credential Attack

Evidence:

```text
Multiple failed login attempts detected
Login originated from an unusual IP address
Login occurred at midnight
```

Expected result:

```text
Threat: Credential Attack
Risk: HIGH
Confidence: 90%
```

### Malware Incident

Evidence:

```text
Malware detected on endpoint
Malicious process started unexpectedly
Unusual outbound connection detected
```

Expected result:

```text
Threat: Malware Activity
Risk: HIGH
Confidence: 100%
```

### Network Anomaly

Evidence:

```text
Unusual outbound network connection
Large volume of data transferred
Connection to unknown external host
```

Expected result:

```text
Threat: Network Anomaly
Risk: HIGH
Confidence: 90%
```

## Testing

Run the test suite using:

```powershell
python -m pytest -q
```

The existing tests cover:

* HIGH-risk investigation
* MEDIUM-risk investigation
* LOW-risk investigation

Backend changes should be regression-tested before being committed.

## Explainable Scoring

The current analyzer uses weighted indicators.

Examples include:

```text
Failed login                 +30
Unusual IP                   +40
After-hours activity         +20
Brute-force activity         +50
Malware                      +40
Malicious process            +30
Suspicious outbound traffic  +30
Large data transfer          +30
Unknown external host        +30
```

The final score is capped at 100.

This approach makes the investigation result deterministic and explainable rather than relying entirely on opaque AI-generated severity decisions.

## Security Considerations

The project follows several security-oriented development principles:

* Secrets are not hardcoded into source code.
* `.env` is excluded from version control.
* The browser does not receive backend API secrets.
* Risk scoring remains deterministic.
* AI reasoning will not replace objective indicator detection.
* Recommendations are advisory and do not automatically execute remediation.
* LLM integration should fail gracefully if unavailable.

## Limitations

The current prototype has several intentional limitations:

* Evidence is manually entered.
* Indicator detection is keyword-based.
* Investigation history is not persistent.
* There is currently no database.
* There is currently no SIEM integration.
* There is currently no threat intelligence feed.
* There is currently no user authentication.
* Reports are exported as text rather than PDF.
* No LLM reasoning service is currently required for the application to operate.

These limitations are appropriate for the current MVP and provide clear areas for future development.

## Future Development

Potential future improvements include:

* LLM-assisted investigation reasoning
* MLflow experiment tracking and model versioning
* MITRE ATT&CK mapping
* IOC extraction
* Threat intelligence enrichment
* SIEM log ingestion
* Authentication log analysis
* Firewall log analysis
* Endpoint telemetry
* Network/PCAP analysis
* Persistent case storage
* Database integration
* PDF investigation reports
* Evidence correlation
* RAG-based historical investigation retrieval
* Analyst feedback mechanisms
* Audit logging

## Planned LLM Integration

A future module such as:

```text
app/ai_reasoner.py
```

can receive structured information from the deterministic engine:

```json
{
  "case_name": "Credential Compromise Investigation",
  "evidence": [
    "Multiple failed login attempts detected",
    "Login originated from an unusual IP address",
    "Login occurred at midnight"
  ],
  "rule_score": 90,
  "risk_level": "HIGH",
  "threat": "Credential Attack",
  "findings": [
    "Multiple failed login attempts detected",
    "Suspicious or unusual IP address detected",
    "Login occurred outside normal hours"
  ]
}
```

The AI reasoning layer can then generate contextual reasoning without replacing deterministic security scoring.

If the AI service fails or no API key is configured, the rule-based investigation should remain fully functional.

## Development Philosophy

The project follows an incremental engineering approach:

```text
Core Engine
    ↓
Testing
    ↓
API
    ↓
Web Interface
    ↓
Demo Features
    ↓
Documentation
    ↓
AI Reasoning
    ↓
Advanced Integrations
```

The goal is to preserve:

* Explainability
* Modularity
* Testability
* Reliability
* Security
* Clear separation between deterministic analysis and AI reasoning

## Project Status

Current MVP status:

```text
Rule-Based Analyzer       ✅
Risk Scoring              ✅
Threat Classification     ✅
Attack Hypothesis         ✅
FastAPI Backend           ✅
Web Dashboard             ✅
Demo Scenarios            ✅
Investigation History     ✅
Report Export             ✅
Automated Tests           ✅
GitHub Repository         ✅
LLM Reasoning Layer       Planned
MLflow Integration        Planned
```

## Capstone Direction

The final project vision is a hybrid cybersecurity investigation assistant that can:

1. Receive security evidence.
2. Detect suspicious indicators.
3. Calculate explainable risk.
4. Classify the likely threat.
5. Correlate evidence.
6. Develop an attack hypothesis.
7. Explain why the activity is suspicious.
8. Recommend analyst investigation steps.
9. Generate an investigation report.
10. Integrate AI reasoning while preserving deterministic security analysis.

---

**AI Investigation Engine — Cybersecurity Investigation and Threat Analysis Prototype**
