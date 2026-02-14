const { exec } = require('child_process');
const os = require('os');
const fs = require('fs');
const { promisify } = require('util');
const execPromise = promisify(exec);

// Parse arguments manually
const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].substring(2);
    const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true;
    params[key] = value;
  }
}

const { action, value, app } = params;
let platform = os.platform(); // 'linux', 'darwin', 'win32'
let isWsl = false;
// Default to standard path, but update for WSL
let powershellPath = 'powershell.exe'; 
let cmdPath = 'cmd.exe';
let taskkillPath = 'taskkill.exe'; // Default
let nircmdPath = 'nircmd.exe'; // Default

// Detect WSL
if (platform === 'linux') {
    try {
        const release = fs.readFileSync('/proc/version', 'utf8').toLowerCase();
        if (release.includes('microsoft') || release.includes('wsl')) {
            isWsl = true;
            platform = 'wsl'; 
            // Use full paths for WSL
            powershellPath = '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe';
            cmdPath = '/mnt/c/Windows/System32/cmd.exe';
            taskkillPath = '/mnt/c/Windows/System32/taskkill.exe'; // Full path for WSL
            nircmdPath = '"/mnt/d/Program Files/nircmd/nircmd.exe"';
        }
    } catch (e) {}
}

async function doTool() {
  if (!action) {
    console.error('Error: --action is required');
    process.exit(1);
  }

  console.log('[Device Control] Platform: ' + platform + ' (WSL: ' + isWsl + ')');
  console.log('[Device Control] Using PowerShell: ' + powershellPath);

  try {
    switch (action) {
      case 'set_volume':
        if (value === undefined) throw new Error('Value required for set_volume');
        await setVolume(value);
        break;
      case 'set_brightness':
        if (value === undefined) throw new Error('Value required for set_brightness');
        await setBrightness(value);
        break;
      case 'open_app':
        if (!app) throw new Error('App name/path required for open_app');
        await openApp(app);
        break;
      case 'close_app':
        if (!app) throw new Error('App name required for close_app');
        await closeApp(app);
        break;
      default:
        console.error('Unknown action: ' + action);
        process.exit(1);
    }
    console.log('Action ' + action + ' completed successfully.');
  } catch (error) {
    console.error('Error executing ' + action + ':', error.message);
    process.exit(1);
  }
}

async function setVolume(val) {
  const v = parseInt(val);
  
  if (platform === 'linux') {
    try {
      await execPromise('pactl set-sink-volume @DEFAULT_SINK@ ' + v + '%');
    } catch (e) {
      await execPromise('amixer sset Master ' + v + '%');
    }
  } else if (platform === 'darwin') {
    await execPromise('osascript -e "set volume output volume ' + v + '"');
  } else if (platform === 'win32' || platform === 'wsl') {
    // Use nircmd.exe for precise volume control - QUOTED path
    // 65535 is 100% volume
    const nircmdVal = Math.floor(65535 * (v / 100));
    const cmd = nircmdPath + ' setsysvolume ' + nircmdVal; // nircmdPath is already quoted
    console.log('Running volume command: ' + cmd);
    await execPromise(cmd);
  }
}

async function setBrightness(val) {
  const v = parseInt(val);
  
  if (platform === 'linux' && !isWsl) {
    // Linux logic... (omitted for brevity)
    throw new Error("Linux brightness logic placeholder");
  } else if (platform === 'darwin') {
    throw new Error("macOS brightness requires 'brightness' CLI tool.");
  } else if (platform === 'win32' || platform === 'wsl') {
    // WmiMonitorBrightnessMethods via PowerShell
    // 1 is the timeout in seconds
    const psCmd = '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, ' + v + ')';
    const cmd = powershellPath + ' -Command "' + psCmd + '"';
    
    console.log('Running: ' + cmd);
    await execPromise(cmd);
  }
}

async function openApp(appName) {
  if (platform === 'linux') {
    const subprocess = exec('"' + appName + '"', { detached: true, stdio: 'ignore' });
    subprocess.unref();
  } else if (platform === 'darwin') {
    await execPromise('open -a "' + appName + '"');
  } else if (platform === 'win32') {
    await execPromise('start "" "' + appName + '"');
  } else if (platform === 'wsl') {
      // Use cmd.exe /c start to launch Windows apps from WSL - QUOTED
      await execPromise(cmdPath + ' /c start "" "' + appName + '"');
  }
}

async function closeApp(appName) {
  if (platform === 'linux' || platform === 'darwin') {
    await execPromise('pkill -f "' + appName + '"');
  } else if (platform === 'win32') {
    await execPromise('taskkill /IM "' + appName + '.exe" /F');
  } else if (platform === 'wsl') {
      // Use full path for taskkill.exe in WSL
      await execPromise(taskkillPath + ' /F /IM "' + appName + '.exe"'); 
  }
}

doTool();
