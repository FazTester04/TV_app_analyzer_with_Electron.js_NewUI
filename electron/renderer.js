const logContainer = document.getElementById("logContainer");
const appendLog = (msg) => {
  logContainer.textContent += msg + "\n";
  logContainer.scrollTop = logContainer.scrollHeight;
};

// Start/Stop Server
document.getElementById("btnStartServer").addEventListener("click", async () => {
  const res = await window.electronAPI.startServer();
  appendLog(res.msg);
});

document.getElementById("btnStopServer").addEventListener("click", async () => {
  const res = await window.electronAPI.stopServer();
  appendLog(res.msg);
});

// Flow selection
let selectedFlow = null;
document.getElementById("btnChooseFlow").addEventListener("click", async () => {
  const path = await window.electronAPI.chooseFlow();
  if (path) {
    selectedFlow = path;
    appendLog("Selected Flow: " + path);
  } else appendLog("No flow selected.");
});

// Run tests
document.getElementById("btnRunTests").addEventListener("click", async () => {
  if (!selectedFlow) return appendLog("Please choose a flow first.");
  appendLog("Running tests using " + selectedFlow);
  const result = await window.electronAPI.runTests(selectedFlow);
  appendLog(result.msg);
});

// Generate report + display both charts
document.getElementById("btnGenerateReport").addEventListener("click", async () => {
  appendLog("Analyzing logs and generating report...");
  const result = await window.electronAPI.generateReport();
  if (result.ok) {
    appendLog("✅ Report generated successfully!");
    if (result.images?.bar)
      document.getElementById("barChart").src = result.images.bar + "?t=" + Date.now();
    if (result.images?.pie)
      document.getElementById("pieChart").src = result.images.pie + "?t=" + Date.now();
  } else appendLog("❌ Failed to generate report.");
});

// Open Flow Builder
document.getElementById("btnCreateFlow").addEventListener("click", async () => {
  appendLog("Opening Flow Builder...");
  const result = await window.electronAPI.runCommand("createFlow");
  appendLog(result);
});

// Open log file
document.getElementById("btnOpenLog").addEventListener("click", async () => {
  await window.electronAPI.openFile("runner/test_log.txt");
});

// Live log streaming
window.electronAPI.onLog((data) => {
  appendLog(`[${data.source}] ${data.text.trim()}`);
});
