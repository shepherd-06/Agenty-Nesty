const { app, BrowserWindow, ipcMain, Tray, Menu } = require('electron')
const { exec } = require('child_process')
const waitOn = require('wait-on')
const path = require('path')

app.commandLine.appendSwitch('disable-gpu')
app.commandLine.appendSwitch('disable-software-rasterizer')

let mainWindow
let settingsWindow
let tray
let statsWindow

const htmlBasePath = path.join(__dirname, 'electron_app', 'html');
const jsBasePath = path.join(__dirname, 'electron_app', 'js');



app.whenReady().then(async () => {
    // Main Chat Window
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 700,
        icon: path.join(__dirname, 'icon.icns'),
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(jsBasePath, 'preload.js') // Secure communication
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
        { label: 'System Stats', click: () => openStatsWindow() },
        { type: 'separator' },
        { role: 'quit' }
    ])
    tray.setToolTip('Agent Nesty')
    tray.setContextMenu(trayMenu)

    // Check system stats every 10 seconds and update tray
    setInterval(checkSystemStats, 10000)
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

    settingsWindow.loadFile(path.join(htmlBasePath, 'settings.html'))
    settingsWindow.once('ready-to-show', () => settingsWindow.show())

    settingsWindow.on('closed', () => {
        settingsWindow = null
    })
}

function openStatsWindow() {
    if (statsWindow) {
        statsWindow.focus()
        return
    }

    statsWindow = new BrowserWindow({
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

    statsWindow.loadFile(path.join(htmlBasePath, 'stats.html'))
    statsWindow.once('ready-to-show', () => statsWindow.show())

    statsWindow.on('closed', () => {
        statsWindow = null
    })
}

// ✅ Fetch System Stats & Update Tray Tooltip
async function checkSystemStats() {
    try {
        const response = await axios.get('http://127.0.0.1:5000/get_system_stats')
        const stats = response.data

        let tooltip = `⚙️ CPU: ${stats.cpu_usage}%  |  🖥 RAM: ${stats.ram_usage}%`
        if (stats.cpu_temp !== "N/A") tooltip += `  |  🌡️ Temp: ${stats.cpu_temp}°C`
        if (stats.fan_speed !== "N/A") tooltip += `  |  🔄 Fan: ${stats.fan_speed} RPM`

        tray.setToolTip(`Agent Nesty - System Monitor\n${tooltip}`)

        // ✅ Trigger alert if CPU usage or temp is high
        if (stats.cpu_usage > 80 || stats.cpu_temp > 85) {
            new Notification({
                title: '⚠️ High System Usage!',
                body: `CPU: ${stats.cpu_usage}%, Temp: ${stats.cpu_temp}°C`,
                icon: path.join(__dirname, 'icon.png')
            }).show()
        }
    } catch (error) {
        console.error("Failed to fetch system stats:", error)
    }
}