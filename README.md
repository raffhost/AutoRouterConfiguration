# ARCTIC — Auto Router Configuration Tool

A desktop application for automated first-time setup of Teltonika routers over a LAN cable.
Instead of clicking through the web interface manually every time, a technician connects the
router, fills in a few fields, and lets the tool handle the rest.

---

## What is this?

Setting up a new Teltonika router always means the same steps: changing the default password,
flashing the correct firmware, selecting the right ISP profile and APN, and checking that the
mobile data connection is working. With multiple routers, this process is slow and repetitive.

ARCTIC automates exactly that — connect the router via LAN, select the options, click a button.

---

## Supported devices

- Teltonika **RUT** series (e.g. RUT240)
- Teltonika **TRB** series (e.g. TRB142)

Both run on RutOS (based on OpenWrt). The tool communicates with the router over SSH using the
`paramiko` library.

---

## What the tool does

- **Connect / Disconnect** — establishes or closes the SSH connection to the router
- **Update** — uploads the selected firmware, tests compatibility with the device first
  (`sysupgrade -T`) and only flashes if the test passes, so an incompatible image can never be
  written to the router by accident
- **Change PW** — sets a new router password
- **Set ISP** — switches the ISP profile (also updates APN and gateway automatically)
- **Set APN** — sets the mobile APN manually and restarts the network interface
- **NETRestart / Reboot** — restarts networking or reboots the router
- **Auto Configuration** — runs the full setup in one go: connect → update firmware → wait for
  reboot → reconnect → change password → set ISP → reconnect → set APN → reconnect. Can be
  cancelled at any point with the **Cancel** button; the log then shows exactly which steps were
  completed and which were not
- **Live status panel** — shows current IP, ISP, APN, firmware version and LAN MAC address, plus
  live checks for data connection, SIM state and network registration state (via `gsmctl`).
  Values can be refreshed and copied to the clipboard

---

## Supported providers and APNs

| Provider | Tariff | APN |
|---|---|---|
| Vodafone | IoT | m2m.vodafone.de |
| o2 | Alle | internet |
| DTAG | Alle | internet.telekom |
| Jola | Multinet (Backup) | 3iot2.com |
| Jola | Vodafone Unlimited UK | internet |
| Jola | Three Unlimited UK | three.co.uk |
| TATA | Alle | move.dataxs.mobi |
| Netia | Unlimited Polen | internet |
| WindTree | Unlimited Italien | internet.wind |
| A1 | Unlimited Österreich | a1.net |
| Digital Republic | Unlimited Schweiz | internet |

---

## Tech stack

- **Python** — main language
- **tkinter + ttk** — desktop GUI (no extra installation needed)
- **paramiko** — SSH connection and command execution
- **JSON** — configuration data (firmware list, ISP profiles, providers/APNs)
- **PyInstaller** — packages the app into a single Windows `.exe`

---

## File structure

```
arctic.py       — GUI (main window, all user interface elements, tooltips)
router.py       — Router class (SSH connection, commands, firmware update, status checks)
config.py       — Labels, tooltips and fonts used in the GUI
config.json     — Firmware list, ISP profiles, providers/APNs, firmware folder path
```

---

## Building the .exe

```
pip install pyinstaller
pyinstaller --onefile --windowed --icon=content/icon.ico --distpath dist_exe --name ARCTIC arctic.py 
```

- `--onefile` bundles everything into a single `ARCTIC.exe`
- `--windowed` suppresses the console window (required for a tkinter GUI app)

The finished executable is created under `dist/ARCTIC.exe`. **`config.json` is not bundled into
the exe on purpose** — copy it into `dist/` next to `ARCTIC.exe` so it can still be edited by
hand after building (e.g. to change the firmware folder path or add new ISP profiles).

`build/`, `dist/` and `*.spec` are regenerated on every build and are excluded via `.gitignore`.

---

## Status

Core functionality complete and tested against real hardware (RUT240): connecting, firmware
updates with compatibility testing, password/ISP/APN changes, full Auto Configuration workflow
with cancel support, and a live status panel.

Open for future improvement:
- Editable firmware list / folder path directly from the GUI, not just via `config.json`
- Icon for the packaged `.exe`
- Testing across additional router models (TRB series)

---

## Development history (high-level)

| Week | Focus |
|---|---|
| Week 2 (29.06.–03.07.) | Project idea defined, GUI library chosen (`tkinter`), first window with `.grid()` |
| Week 3 (06.07.–10.07.) | Config moved to `config.json`, `Router` class with SSH connection, threading/queue basics |
| Week 4 (13.07.–16.07.) | Error handling, status indicators, thread-safe log/GUI queues, workshop feedback |
| Week 5 (20.07.–24.07.) | Auto Configuration workflow, cancel support, firmware compatibility test, structural cleanup |
| Week 6 (27.07.–28.07.) | Live status panel (router data + SIM/network checks), packaged as `.exe`. Technically, the project is finished, but I might add something new in the future.|
