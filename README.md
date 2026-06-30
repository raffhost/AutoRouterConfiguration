# AutoRouterCOnfiguration

A tool for automatically setting up Teltonika routers (RUT/TRB) over a LAN
cable — no need to click through the web interface by hand.

## What is this?

Setting up a new Teltonika router always means the same steps: changing the
password, updating the firmware, setting the internet provider (APN), and
checking that everything works. With multiple routers, this takes a long
time and is repetitive.

This tool automates exactly that. You connect the router with a LAN cable,
click a button — and the tool does the rest.

## Which routers?

- **Teltonika RUT series** (e.g. RUT240)
- **Teltonika TRB series** (e.g. TRB142)

Both run on RutOS, which is based on OpenWrt. Because of that, the same
commands (UCI or REST API) work on both series — small differences between
models are checked individually when needed.

## What the tool does

1. Logs in with the factory password (`admin` / `admin01`)
2. Sets a new, fixed password
3. Updates the firmware
4. Logs in again after the reboot and sets the password once more
   (because the update resets the settings)
5. Sets the internet provider (ISP) and the correct APN
6. Checks that the internet connection is working

## The app

Three buttons:

- **Update** — runs the full setup process
- **Create RMS** — not automated yet, planned for later
- **Connect** — checks whether the router is online

Each button shows green (success) or red (failed). Next to it, there's an
overview with all the important info about the router (password, name,
IP address, firmware used, MAC address) for quick copying.

## Tools used

- **Python** — programming language
- **requests** — for communicating with the router (REST API)
- **paramiko** — fallback over SSH, in case the REST API isn't available
- **customtkinter** — for the app's buttons and window

## Status

Early stage project (training/internship work). Currently building the app
interface, with the connection to the routers coming next.
