const { app, BrowserWindow, ipcMain, Tray, Menu } = require('electron')
const { exec } = require('child_process')
const waitOn = require('wait-on')
const path = require('path')

app.commandLine.appendSwitch('disable-gpu')
app.commandLine.appendSwitch('disable-software-rasterizer')

let mainWindow
let settingsWindow
let tray

app.whenReady().then(async () => {
    // Main Chat Window
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 700,
        icon: path.join(__dirname, 'icon.icns'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js') // Secure communication
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

    // Create macOS Menu Bar Icon (Tray)
    tray = new Tray(path.join(__dirname, 'icon.png'))
    const trayMenu = Menu.buildFromTemplate([
        {
            label: 'Show Message',
            click: () => {
                mainWindow.webContents.executeJavaScript(`alert('Agent Nesty is Running!')`)
            }
        },
        {
            label: 'Open Settings',
            click: () => {
                openSettingsWindow()
            }
        },
        { type: 'separator' },
        { role: 'quit' }
    ])
    tray.setToolTip('Agent Nesty')
    tray.setContextMenu(trayMenu)
})

// ✅ Function to Open Settings Window
ipcMain.on('open-settings', () => {
    openSettingsWindow()
})

function openSettingsWindow() {
    if (settingsWindow) {
        settingsWindow.focus()
        return
    }

    settingsWindow = new BrowserWindow({
        width: 400,
        height: 300,
        parent: mainWindow,
        modal: true,
        show: false,
        resizable: false,
        webPreferences: {
            nodeIntegration: true
        }
    })

    settingsWindow.loadFile('settings.html')
    settingsWindow.once('ready-to-show', () => settingsWindow.show())

    settingsWindow.on('closed', () => {
        settingsWindow = null
    })
}
