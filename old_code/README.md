# ARCTIC — Auto Router Configuration Tool

A desktop application for automated first-time setup of Teltonika routers over a LAN cable.
Instead of clicking through the web interface manually every time, a technician connects the
router, fills in the required fields, and lets the tool handle the rest.

---

## What is this?

Setting up a new Teltonika router always means the same steps: changing the default password,
flashing the correct firmware, selecting the right ISP profile and APN, and checking that the
mobile data connection is working. With multiple routers, this process is slow and repetitive.

ARCTIC automates exactly that — connect the router via LAN, select the options, click a button.

---

## Supported devices

- **Teltonika RUT series** — RUT2xx, RUT36x, RUT361
- **Teltonika TRB series** — TRB500, TRB501

Both run on RutOS (based on OpenWrt). The tool communicates with the router over SSH using
the Paramiko library. REST API support is planned for a later stage.

---

## What the tool does

1. Connects to the router via SSH (default: `root` / `admin01`)
2. Changes the password to the company password
3. Flashes the correct firmware for the selected model (without keeping old settings)
4. Waits for the router to reboot, then logs in again and sets the password once more
5. Sets the ISP profile and the correct APN for the selected mobile provider
6. Checks that the mobile data connection is working

---

## The app

Three main actions:

- **Connect** — establishes SSH connection to the router
- **Update** — runs the full setup (firmware + password + APN)
- **Status light** — shows green when connected, red when not (checks every second automatically)

The left side of the window handles all input: firmware selection, ISP profile, mobile provider
and APN, and the router password. The right side is reserved for a status panel (in progress).

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
- **tkinter + ttk** — desktop GUI
- **paramiko** — SSH connection to the router
- **JSON** — configuration data (firmware list, ISP profiles, providers/APNs)

---

## File structure

```
app.py         — GUI (main window, all user interface elements)
router.py      — Router class (SSH connection, commands, firmware update)
config.json    — All data: firmware files, ISP profiles, providers and APNs
```

---

## Status

Active development — internship project (Ausbildungspraktikum).
GUI is mostly complete. Router connection via SSH is working.
Firmware flashing and password change are the next steps.

---

## Development history

| Date | What happened |
|---|---|
| 30.06.2026 | Project idea defined. Chose to automate Teltonika router setup. Created repo. |
| 01.07.2026 | Started learning tkinter. First window with buttons and APN combobox using `.grid()`. |
| 02.07.2026 | Restructured code, moved config to `Config.py`, removed RMS class, switched to `.grid()` layout. |
| 03.07.2026 | Replaced `.grid()` with `.place()` for easier positioning. Added separators, ISP selection with auto IP display. Created `router.py` with paramiko skeleton. |
| 06.07.2026 | Moved all data to `config.json`. Added provider/APN selection (dynamic, based on chosen provider). Firmware list now loaded from JSON. |
| 07.07.2026 | Connected `Router` class to GUI. Added Connect and Update buttons, password entry field, and status light (auto-updates every second via `self.after()`). |
