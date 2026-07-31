# ARCTIC — Auto Router Configuration Tool

A desktop application for automated first-time setup of Teltonika routers over a LAN cable.
Instead of clicking through the web interface manually every time, connect the router, fill in
a few fields, and let the tool handle the rest.

**License:** Personal / non-commercial use only. See [LICENSE.txt](LICENSE.txt).

---

## Download

Windows installer (recommended): see the [Releases](../../releases) page, download and run
`ARCTIC_Setup.exe`.

Alternatively, install via pip:
```
pip install arctic-router-tool
arctic
```

---

## What the tool does

- **Connect / Disconnect** — establishes or closes the SSH connection to the router
- **Update** — uploads a firmware file, tests compatibility with the device first
  (`sysupgrade -T`) and only flashes if the test passes, so an incompatible image can never be
  written to the router by accident
- **Browse firmware** — pick any local `.bin` firmware file via a file dialog; optionally save it
  to the configuration for reuse, with automatic duplicate detection
- **Change PW** — sets a new router password
- **Set ISP** — switches the ISP profile (also updates APN and gateway automatically)
- **Set APN** — sets the mobile APN manually and restarts the network interface
- **NETRestart / Reboot** — restarts networking or reboots the router
- **Auto Configuration** — runs the full setup in one go: connect → update firmware → wait for
  reboot → reconnect → change password → set ISP → reconnect → set APN → reconnect. Can be
  cancelled at any point; the log then shows exactly which steps were completed and which were
  not
- **Live status panel** — shows current IP, ISP, APN, firmware version, LAN MAC, serial number
  and (optionally) IMEI, plus live checks for data connection, SIM state and network registration
  state. Values can be refreshed and copied to the clipboard

---

## Supported devices

- Teltonika **RUT** series (tested on RUT240)
- Teltonika **TRB** series

Both run on RutOS (based on OpenWrt). The tool communicates with the router over SSH using the
`paramiko` library.

---

## Building from source

Requires Python 3.10+.

```
pip install -r requirements.txt
```

Run directly:
```
python arctic.py
```

Build a standalone `.exe` (Windows):
```
build_exe.bat
```
This installs PyInstaller automatically if it's missing, builds `ARCTIC.exe` in the project
folder, and cleans up temporary build files afterwards. The `arctic_config.json` next to it can
be edited by hand (e.g. to add ISP profiles) without rebuilding the exe.

---

## Tech stack

- **Python** — main language
- **tkinter + ttk** — desktop GUI (no extra installation needed)
- **paramiko** — SSH connection and command execution
- **threading** — handles background operations without blocking the main application
- **queue** — manages safe data exchange between threads and the GUI
- **JSON** — configuration data (firmware list, ISP profiles, providers/APNs)
- **PyInstaller** — packages the app into a single Windows `.exe`
- **Inno Setup** — builds the Windows installer

---

## File structure

```
arctic.py              — GUI (main window, all UI elements, tooltips)
router.py              — Router class (SSH connection, commands, firmware update, status checks)
config.py              — GUI configuration (labels, tooltips, fonts)
arctic_config.json     — Firmware list, ISP profiles, providers/APNs
build_exe.bat          — One-click build script (PyInstaller)
icon.ico               — Application icon
README.md              — Project documentation
LICENSE.txt            — License information
.gitignore             — Git ignored files configuration
```

---

## Status

Core functionality complete and tested against real hardware: connecting, firmware updates with
compatibility testing, password/ISP/APN changes, full Auto Configuration workflow with cancel
support, custom firmware file selection, and a live status panel.

Open for future improvement:
- Editable ISP/APN profiles directly from the GUI, not just via `arctic_config.json`
- Testing across additional router models (TRB series)
