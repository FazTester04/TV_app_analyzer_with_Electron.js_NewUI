const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('electronAPI', {
  startServer: () => ipcRenderer.invoke('start-server'),
  stopServer: () => ipcRenderer.invoke('stop-server'),
  runCommand: (command) => ipcRenderer.invoke('run-command', command),
  chooseFlow: () => ipcRenderer.invoke('choose-flow'),
  runTests: (flowPath) => ipcRenderer.invoke('run-tests', flowPath),
  generateReport: () => ipcRenderer.invoke('generate-report'),
  openFile: (path) => ipcRenderer.invoke('open-file', path),
  onLog: (cb) => ipcRenderer.on('proc-log', (e, msg) => cb(msg)),
  onProcExit: (cb) => ipcRenderer.on('proc-exit', (e, data) => cb(data))
});
