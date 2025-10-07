const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let serverProc = null;
let runnerProc = null;

const PROJECT_ROOT = path.resolve(__dirname, '..');
const PYTHON_CMD = 'python';

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });
  mainWindow.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(createWindow);

// Start Flask mock server
ipcMain.handle('start-server', (event) => {
  if (serverProc && !serverProc.killed) {
    return { ok: false, msg: 'Server already running' };
  }
  const script = path.join(PROJECT_ROOT, 'mock_tv', 'server.py');
  serverProc = spawn(PYTHON_CMD, [script], { cwd: PROJECT_ROOT });
  serverProc.stdout.on('data', data => mainWindow.webContents.send('proc-log', { source: 'server', text: data.toString() }));
  serverProc.stderr.on('data', data => mainWindow.webContents.send('proc-log', { source: 'server', text: data.toString() }));
  serverProc.on('close', code => mainWindow.webContents.send('proc-exit', { source: 'server', code }));
  return { ok: true, msg: 'Server started' };
});

// Stop Flask server
ipcMain.handle('stop-server', () => {
  if (serverProc && !serverProc.killed) {
    serverProc.kill();
    serverProc = null;
    return { ok: true, msg: 'Server terminated' };
  }
  return { ok: false, msg: 'No server running' };
});

// Choose JSON Flow File
ipcMain.handle('choose-flow', async () => {
  const res = await dialog.showOpenDialog(mainWindow, {
    title: 'Select Flow JSON',
    defaultPath: path.join(PROJECT_ROOT, 'examples'),
    filters: [{ name: 'JSON', extensions: ['json'] }],
    properties: ['openFile']
  });
  if (res.canceled || res.filePaths.length === 0) return null;
  return res.filePaths[0];
});

// Run Tests
ipcMain.handle('run-tests', (event, flowPath) => {
  if (runnerProc && !runnerProc.killed) {
    return { ok: false, msg: 'Runner already running' };
  }
  const script = path.join(PROJECT_ROOT, 'runner', 'test_runner.py');
  runnerProc = spawn(PYTHON_CMD, [script, flowPath], { cwd: PROJECT_ROOT });
  runnerProc.stdout.on('data', data => mainWindow.webContents.send('proc-log', { source: 'runner', text: data.toString() }));
  runnerProc.stderr.on('data', data => mainWindow.webContents.send('proc-log', { source: 'runner', text: data.toString() }));
  runnerProc.on('close', code => mainWindow.webContents.send('proc-exit', { source: 'runner', code }));
  return { ok: true, msg: 'Runner started' };
});

// Analyze logs + generate report
ipcMain.handle('generate-report', async () => {
  const analyzer = path.join(PROJECT_ROOT, 'analyzer', 'log_analyzer.py');
  const reporter = path.join(PROJECT_ROOT, 'reports', 'report_generator.py');
  const logPath = path.join(PROJECT_ROOT, 'runner', 'test_log.txt');

  const aProc = spawn(PYTHON_CMD, [analyzer, logPath], { cwd: PROJECT_ROOT });
  aProc.stdout.on('data', d => mainWindow.webContents.send('proc-log', { source: 'analyzer', text: d.toString() }));
  aProc.stderr.on('data', d => mainWindow.webContents.send('proc-log', { source: 'analyzer', text: d.toString() }));
  await new Promise(resolve => aProc.on('close', resolve));

  const rProc = spawn(PYTHON_CMD, [reporter, logPath], { cwd: PROJECT_ROOT });
  rProc.stdout.on('data', d => mainWindow.webContents.send('proc-log', { source: 'report', text: d.toString() }));
  rProc.stderr.on('data', d => mainWindow.webContents.send('proc-log', { source: 'report', text: d.toString() }));
  await new Promise(resolve => rProc.on('close', resolve));

  // ✅ Return both chart paths
  const bar = path.resolve(PROJECT_ROOT, 'reports', 'pass_fail.png');
  const pie = path.resolve(PROJECT_ROOT, 'reports', 'pass_fail_pie.png');
  return { ok: true, images: { bar, pie } };
});

// Flow Builder integration
ipcMain.handle('run-command', async (event, command) => {
  if (command === 'createFlow') {
    const script = path.join(PROJECT_ROOT, 'tools', 'flow_builder.py');
    const proc = spawn(PYTHON_CMD, [script], { cwd: PROJECT_ROOT });
    proc.stdout.on('data', d => mainWindow.webContents.send('proc-log', { source: 'flow', text: d.toString() }));
    proc.stderr.on('data', d => mainWindow.webContents.send('proc-log', { source: 'flow', text: d.toString() }));
    await new Promise(resolve => proc.on('close', resolve));
    return 'Flow Builder closed.';
  }
  return 'Unknown command.';
});

ipcMain.handle('open-file', (event, filePath) => {
  if (!fs.existsSync(filePath)) return { ok: false, msg: 'File not found' };
  shell.openPath(filePath);
  return { ok: true };
});

app.on('before-quit', () => {
  if (serverProc && !serverProc.killed) serverProc.kill();
  if (runnerProc && !runnerProc.killed) runnerProc.kill();
});
