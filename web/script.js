const API_URL = "http://127.0.0.1:8000/investigate";


const scenarios = {

    credential: {

        name: "Credential Compromise Investigation",

        evidence: [
            "Multiple failed login attempts detected",
            "Login originated from an unusual IP address",
            "Login occurred at midnight"
        ]

    },


    malware: {

        name: "Malware Incident Investigation",

        evidence: [
            "Malware detected on endpoint",
            "Malicious process started unexpectedly",
            "Unusual outbound connection detected"
        ]

    },


    network: {

        name: "Network Anomaly Investigation",

        evidence: [
            "Unusual outbound network connection",
            "Large volume of data transferred",
            "Connection to unknown external host"
        ]

    }

};


let investigationHistory = [];

let currentResult = null;


function loadScenario(type) {

    const scenario = scenarios[type];

    document.getElementById("caseName").value =
        scenario.name;

    document.getElementById("evidence").value =
        scenario.evidence.join("\n");

    document
        .getElementById("caseName")
        .scrollIntoView({
            behavior: "smooth"
        });

}


const button =
    document.getElementById("investigateBtn");


button.addEventListener("click", async () => {

    const caseName =
        document.getElementById("caseName").value.trim();


    const evidenceText =
        document.getElementById("evidence").value.trim();


    if (!caseName || !evidenceText) {

        alert(
            "Please provide a case name and evidence."
        );

        return;

    }


    const evidence =
        evidenceText
            .split("\n")
            .map(item => item.trim())
            .filter(item => item.length > 0);


    button.disabled = true;

    button.textContent =
        "ANALYZING...";


    try {

        const response =
            await fetch(
                API_URL,
                {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        case_name: caseName,
                        evidence: evidence
                    })

                }
            );


        if (!response.ok) {

            throw new Error(
                "Investigation request failed."
            );

        }


        const result =
            await response.json();


        currentResult = result;

        investigationHistory.unshift(result);

        displayResults(result);

        displayHistory();


    } catch (error) {

        alert(
            "Could not connect to the investigation engine.\n\n"
            + error.message
        );


    } finally {

        button.disabled = false;

        button.textContent =
            "START INVESTIGATION";

    }

});


function displayResults(result) {

    document
        .getElementById("results")
        .classList.remove("hidden");


    document.getElementById("resultCase").textContent =
        result.case_name;


    document.getElementById("riskLevel").textContent =
        result.risk_level;


    document.getElementById("confidence").textContent =
        result.confidence + "%";


    document.getElementById("threat").textContent =
        result.threat;


    document.getElementById("hypothesis").textContent =
        result.attack_hypothesis;


    const riskBadge =
        document.getElementById("riskBadge");


    riskBadge.textContent =
        result.risk_level;


    riskBadge.className =
        "risk-badge " +
        result.risk_level.toLowerCase();


    const findings =
        document.getElementById("findings");


    findings.innerHTML = "";


    result.findings.forEach(finding => {

        const li =
            document.createElement("li");

        li.textContent =
            finding;

        findings.appendChild(li);

    });


    const recommendations =
        document.getElementById(
            "recommendations"
        );


    recommendations.innerHTML = "";


    result.recommendations.forEach(
        recommendation => {

            const li =
                document.createElement("li");

            li.textContent =
                recommendation;

            recommendations.appendChild(li);

        }
    );


    document
        .getElementById("results")
        .scrollIntoView({
            behavior: "smooth"
        });

}


function displayHistory() {

    const history =
        document.getElementById("history");


    if (investigationHistory.length === 0) {

        history.innerHTML =
            '<div class="empty-history">No investigations performed yet.</div>';

        return;

    }


    history.innerHTML = "";


    investigationHistory.forEach(
        (result, index) => {

            const item =
                document.createElement("div");

            item.className =
                "history-item";


            item.innerHTML = `

                <div class="history-number">
                    #${String(
                        investigationHistory.length - index
                    ).padStart(3, "0")}
                </div>

                <div class="history-info">

                    <strong>
                        ${result.case_name}
                    </strong>

                    <span>
                        ${result.threat}
                    </span>

                </div>

                <div
                    class="history-risk ${result.risk_level.toLowerCase()}"
                >
                    ${result.risk_level}
                </div>

                <div class="history-confidence">
                    ${result.confidence}%
                </div>

            `;


            history.appendChild(item);

        }
    );

}


document
    .getElementById("exportBtn")
    .addEventListener("click", () => {

        if (!currentResult) {
            return;
        }


        const report = `

AI INVESTIGATION ENGINE
=======================

CASE
${currentResult.case_name}

RISK LEVEL
${currentResult.risk_level}

CONFIDENCE
${currentResult.confidence}%

THREAT CLASS
${currentResult.threat}

ATTACK HYPOTHESIS
${currentResult.attack_hypothesis}

FINDINGS
${currentResult.findings
    .map(item => "- " + item)
    .join("\n")}

RECOMMENDED RESPONSE
${currentResult.recommendations
    .map(item => "- " + item)
    .join("\n")}

=======================
Generated by AI Investigation Engine
        `;


        const blob =
            new Blob(
                [report],
                { type: "text/plain" }
            );


        const url =
            URL.createObjectURL(blob);


        const link =
            document.createElement("a");


        link.href = url;

        link.download =
            "investigation-report.txt";


        link.click();


        URL.revokeObjectURL(url);

    });


displayHistory();
