---
name: device-control
description: Expose safe device actions (volume, brightness, open/close apps) for personal automation.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎛️",
        "requires": { "bins": ["node"] },
      },
  }
---

# Device Control Skill

Control device volume, brightness, and applications via command line.

## Tool API

### device_control
Execute a device control action.

- **Parameters:**
  - `action` (string, required): One of `set_volume`, `change_volume`, `set_brightness`, `open_app`, `close_app`.
  - `value` (string/number, optional): The value for the action (e.g., percentage for volume/brightness).
  - `app` (string, optional): The application name or path (required for open/close actions).

**Usage:**

```bash
node skills/device-control/ctl.js --action set_volume --value 50
node skills/device-control/ctl.js --action open_app --app "firefox"
node skills/device-control/ctl.js --action close_app --app "firefox"
```
