const { app, BrowserWindow } = require('electron')
const { exec } = require('child_process')
const waitOn = require('wait-on')

app.commandLine.appendSwitch('disable-gpu')
app.commandLine.appendSwitch('disable-software-rasterizer')


let mainWindow

app.whenReady().then(async () => {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 700,
        webPreferences: {
            nodeIntegration: true
        }
    })

    // Start Flask in the background
    console.log("🚀 Starting Flask server...")
    const flaskProcess = exec("python3 app.py")

    // Wait for Flask to be ready before opening Electron
    await waitOn({ resources: ['http://127.0.0.1:5000'], timeout: 20000 })
        .then(() => {
            console.log("✅ Flask server is running. Opening Electron App...")
            mainWindow.loadURL('http://127.0.0.1:5000')
        })
        .catch(err => {
            console.error("❌ Flask did not start in time:", err)
            mainWindow.loadURL("data:text/html,Flask server failed to start. Try restarting.")
        })
})
