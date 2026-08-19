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

const bootScreen = document.getElementById("bootScreen");
const appShell = document.getElementById("appShell");
const initializeBtn = document.getElementById("initializeBtn");
const bootSequence = document.getElementById("bootSequence");
const bootProgress = document.getElementById("bootProgress");
const bootProgressBar = document.getElementById("bootProgressBar");
const bootProgressValue = document.getElementById("bootProgressValue");
const analysisSequence = document.getElementById("analysisSequence");
const investigateBtn = document.getElementById("investigateBtn");

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function showScreen(targetId) {
    document.querySelectorAll(".screen").forEach(screen => {
        screen.classList.remove("active-screen");
    });

    document.querySelectorAll(".rail-link").forEach(link => {
        link.classList.toggle("active", link.dataset.target === targetId);
    });

    const target = document.getElementById(targetId);
    if (target) {
        target.classList.add("active-screen");
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
}

initializeBtn.addEventListener("click", async () => {
    initializeBtn.classList.add("hidden");
    bootProgress.classList.remove("hidden");
    bootSequence.classList.remove("hidden");

    const title = document.querySelector(".boot-title");
    title.classList.add("glitch");
    setTimeout(() => title.classList.remove("glitch"), 700);

    const rows = [...bootSequence.querySelectorAll("div")];
    const checkpoints = [18, 43, 71, 100];

    for (let i = 0; i < rows.length; i++) {
        const status = rows[i].querySelector("b");
        status.textContent = "PROCESSING";

        const target = checkpoints[i];
        const start = i === 0 ? 0 : checkpoints[i - 1];

        for (let value = start; value <= target; value += 3) {
            const shown = Math.min(value, target);
            bootProgressBar.style.width = `${shown}%`;
            bootProgressValue.textContent = `${shown}%`;
            await sleep(20);
        }

        if (i === 0) status.textContent = "VERIFIED";
        if (i === 1) status.textContent = "ONLINE";
        if (i === 2) status.textContent = "OPTIONAL";
        if (i === 3) status.textContent = "READY";

        await sleep(140);
    }

    bootProgressBar.style.width = "100%";
    bootProgressValue.textContent = "100%";

    await sleep(420);
    bootScreen.style.opacity = "0";
    bootScreen.style.transform = "scale(1.025)";
    bootScreen.style.transition = "opacity 0.65s ease, transform 0.65s ease";
    await sleep(680);

    bootScreen.classList.add("hidden");
    appShell.classList.remove("hidden");
});

document.querySelectorAll(".rail-link").forEach(link => {
    link.addEventListener("click", () => showScreen(link.dataset.target));
});

document.getElementById("launchInvestigation").addEventListener("click", () => {
    showScreen("investigationPanel");
});

document.getElementById("showArchitecture").addEventListener("click", () => {
    document.getElementById("architecturePanel").classList.toggle("hidden");
});

document.getElementById("newCaseBtn").addEventListener("click", () => {
    document.getElementById("caseName").value = "";
    document.getElementById("evidence").value = "";
    document.getElementById("results").classList.add("hidden");
    document.getElementById("caseName").focus();
    window.scrollTo({ top: 0, behavior: "smooth" });
});

function loadScenario(type) {
    const scenario = scenarios[type];
    document.getElementById("caseName").value = scenario.name;
    document.getElementById("evidence").value = scenario.evidence.join("\n");
    document.getElementById("caseName").focus();
}

async function runAnalysisAnimation() {
    const steps = [
        document.getElementById("stepRule"),
        document.getElementById("stepRisk"),
        document.getElementById("stepThreat"),
        document.getElementById("stepAI")
    ];

    steps.forEach(step => step.textContent = "WAITING");
    analysisSequence.classList.remove("hidden");

    const labels = ["VERIFIED", "CALCULATED", "CLASSIFIED", "REQUESTED"];

    for (let i = 0; i < steps.length; i++) {
        steps[i].textContent = "PROCESSING";
        await sleep(180);
        steps[i].textContent = labels[i];
    }
}

investigateBtn.addEventListener("click", async () => {
    const caseName = document.getElementById("caseName").value.trim();
    const evidenceText = document.getElementById("evidence").value.trim();

    if (!caseName || !evidenceText) {
        alert("Please provide a case name and security evidence.");
        return;
    }

    const evidence = evidenceText
        .split("\n")
        .map(item => item.trim())
        .filter(Boolean);

    investigateBtn.disabled = true;
    investigateBtn.querySelector("span").textContent = "ANALYZING...";
    document.getElementById("results").classList.add("hidden");

    try {
        const animationPromise = runAnalysisAnimation();

        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ case_name: caseName, evidence })
        });

        if (!response.ok) {
            throw new Error("Investigation request failed.");
        }

        const result = await response.json();

        await animationPromise;
        await sleep(180);

        analysisSequence.classList.add("hidden");
        currentResult = result;
        investigationHistory.unshift(result);

        displayResults(result);
        displayHistory();

    } catch (error) {
        analysisSequence.classList.add("hidden");
        alert("Could not connect to the investigation engine.\n\n" + error.message);

    } finally {
        investigateBtn.disabled = false;
        investigateBtn.querySelector("span").textContent = "INITIATE ANALYSIS";
    }
});

function displayResults(result) {
    const results = document.getElementById("results");
    results.classList.remove("hidden");

    document.getElementById("resultCase").textContent = result.case_name;
    document.getElementById("riskLevel").textContent = result.risk_level;
    document.getElementById("confidence").textContent = result.confidence;
    document.getElementById("threat").textContent = result.threat;
    document.getElementById("hypothesis").textContent = result.attack_hypothesis;

    const riskBadge = document.getElementById("riskBadge");
    riskBadge.textContent = result.risk_level;
    riskBadge.className = "risk-badge " + result.risk_level.toLowerCase();

    const riskOrbit = document.getElementById("riskOrbit");
    document.querySelector(".risk-console").dataset.level = result.risk_level;
    const score = Math.max(0, Math.min(100, Number(result.confidence) || 0));
    let riskColor = "#2dd4a8";

    if (result.risk_level === "HIGH") riskColor = "#ff5d6c";
    else if (result.risk_level === "MEDIUM") riskColor = "#f5a524";

    riskOrbit.style.setProperty("--risk-angle", `${score * 3.6}deg`);
    riskOrbit.style.setProperty("--risk-color", riskColor);

    renderList("findings", result.findings);
    renderList("recommendations", result.recommendations);

    const aiStatus = document.getElementById("aiStatus");
    const aiSummary = document.getElementById("aiSummary");
    const aiReasoning = document.getElementById("aiReasoning");
    const aiSteps = document.getElementById("aiSteps");

    aiSteps.innerHTML = "";

    if (result.ai_available) {
        aiStatus.textContent = "AI ONLINE";
        aiStatus.className = "ai-status online";
        aiSummary.textContent = result.ai_summary || "No AI summary returned.";
        aiReasoning.textContent = result.ai_reasoning || "No AI reasoning returned.";

        (result.ai_investigation_steps || []).forEach(step => {
            const li = document.createElement("li");
            li.textContent = step;
            aiSteps.appendChild(li);
        });

        if (!result.ai_investigation_steps?.length) {
            const li = document.createElement("li");
            li.textContent = "No additional AI investigation steps returned.";
            aiSteps.appendChild(li);
        }

    } else {
        aiStatus.textContent = "AI FALLBACK";
        aiStatus.className = "ai-status offline";
        aiSummary.textContent = "Gemini reasoning is unavailable. Deterministic investigation remains active.";
        aiReasoning.textContent = "Risk scoring, threat classification and findings were produced by the local rule engine.";

        const li = document.createElement("li");
        li.textContent = "Continue investigation using deterministic findings and recommendations.";
        aiSteps.appendChild(li);
    }

    results.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderList(id, items) {
    const target = document.getElementById(id);
    target.innerHTML = "";

    (items || []).forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        target.appendChild(li);
    });
}

function displayHistory() {
    const history = document.getElementById("history");

    if (investigationHistory.length === 0) {
        history.innerHTML = '<div class="empty-history">NO INVESTIGATIONS RECORDED</div>';
        return;
    }

    history.innerHTML = "";

    investigationHistory.forEach((result, index) => {
        const item = document.createElement("div");
        item.className = "history-item";

        item.innerHTML = `
            <div class="history-info">
                <strong>${escapeHtml(result.case_name)}</strong>
                <span>#${String(investigationHistory.length - index).padStart(3, "0")}</span>
            </div>
            <div class="history-number">${escapeHtml(result.threat)}</div>
            <div class="history-risk ${result.risk_level.toLowerCase()}">${escapeHtml(result.risk_level)}</div>
            <div class="history-confidence">${Number(result.confidence)} / 100</div>
        `;

        history.appendChild(item);
    });
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

document.getElementById("exportBtn").addEventListener("click", () => {
    if (!currentResult) return;

    const report = `
AI INVESTIGATION ENGINE
=======================

CASE
${currentResult.case_name}

RISK LEVEL
${currentResult.risk_level}

RISK SCORE
${currentResult.confidence}/100

THREAT CLASS
${currentResult.threat}

ATTACK HYPOTHESIS
${currentResult.attack_hypothesis}

FINDINGS
${currentResult.findings.map(item => "- " + item).join("\n")}

RECOMMENDED RESPONSE
${currentResult.recommendations.map(item => "- " + item).join("\n")}

AI-ASSISTED ANALYSIS
AI STATUS
${currentResult.ai_available ? "AVAILABLE" : "FALLBACK / UNAVAILABLE"}

AI SUMMARY
${currentResult.ai_available ? currentResult.ai_summary : "Gemini reasoning was unavailable. Rule-based analysis remained active."}

AI REASONING
${currentResult.ai_available ? currentResult.ai_reasoning : "Deterministic security findings were used without LLM enrichment."}

AI INVESTIGATION STEPS
${currentResult.ai_available
    ? (currentResult.ai_investigation_steps || []).map(item => "- " + item).join("\n")
    : "- Continue investigation using deterministic findings and recommendations."}

=======================
Generated by AI Investigation Engine
`;

    const blob = new Blob([report], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "investigation-report.txt";
    link.click();

    URL.revokeObjectURL(url);
});

displayHistory();

const cursorGlow = document.getElementById("cursorGlow");
window.addEventListener("pointermove", event => {
    if (!cursorGlow) return;
    cursorGlow.style.left = `${event.clientX}px`;
    cursorGlow.style.top = `${event.clientY}px`;
});

function updateStreamClock() {
    const target = document.getElementById("streamClock");
    if (!target) return;
    const now = new Date();
    target.textContent = now.toLocaleTimeString([], {
        hour12: false,
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });
}
setInterval(updateStreamClock, 1000);
updateStreamClock();
