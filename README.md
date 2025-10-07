#  TV App Test & Log Analyzer  


---

## 🚀 Quick Start

1.  Create and activate a virtual environment  
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the dashboard (Python GUI)**  
   ```bash
   python dashboard/dashboard.py
   ```

4. **Or launch the modern Electron GUI (requires Node.js)**  
   ```bash
   cd electron
   npm install
   npm start
   ```

---

## Project Structure

```
tv-test-analyzer/
│
├── dashboard/               # Tkinter dashboard (classic Python GUI)
│   └── dashboard.py
│
├── tools/                   # Tools and utilities
│   └── flow_builder.py      # Interactive JSON Flow Builder
│
├── runner/                  # Test execution engine
│   ├── test_runner.py       # Runs test flows and logs results
│   └── test_log.txt         # Test output log
│
├── mock_tv/                 # Flask mock TV API server
│   └── server.py
│
├── analyzer/                # Log and report analysis
│   └── log_analyzer.py
│
├── reports/                 # Charts and report generator
│   ├── report_generator.py
│   ├── pass_fail.png
│   └── pass_fail_pie.png
│
├── examples/                # Sample test flow files
│   └── sample_flow.json
│
├── electron_app/            # Modern Electron GUI
│   ├── main.js              # Electron main process
│   ├── preload.js           # IPC bridge between main and renderer
│   ├── renderer.js          # Frontend logic
│   ├── index.html           # GUI interface
│   ├── package.json         # Electron app metadata
│   └── assets/
│
└── README.md
```

---

## Reports & Charts

After tests:
1. Logs are saved to `runner/test_log.txt`
2. Run analysis:
   ```bash
   python analyzer/log_analyzer.py runner/test_log.txt
   python reports/report_generator.py runner/test_log.txt
   ```
3. Output includes:
   - `reports/pass_fail.png` (bar chart)
   - `reports/pass_fail_pie.png` (pie chart)

Both charts are viewable inside the Electron dashboard.

---

## Electron Integration

- Communicates between **frontend (renderer)** and **backend (Python)** using **IPC (Inter-Process Communication)**.
- Launches and manages Python subprocesses for:
  - Starting/stopping Flask mock server  
  - Running test flows  
  - Generating reports and charts  

Start with:
```bash
cd electron_app
npm install
npm start
```

---

## Building an EXE (Windows)

To package the Electron app:
```bash
npm run make
```
or manually with:
```bash
npx electron-packager . "TV-Test-Analyzer" --platform=win32 --arch=x64 --icon=assets/icon.ico --overwrite
```

Output will appear in `/release-builds/` as a standalone `.exe` ready to distribute.

---

## Requirements

- **Python 3.9+**
- **Flask**
- **requests**
- **tkinter**
- **pandas, matplotlib**
- **Node.js 18+** (for Electron)


---

##  Author

**Fazni Alif** — *Sony TV R&D*  
Demonstrates an end-to-end automation system integrating **Python**, **Flask**, and **Electron**  
