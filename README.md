<div align="center">

```text
██╗██╗     ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗██████╗ ████████╗██╗    ██████╗  ██████╗  ██████╗███╗   ██╗
██║██║     ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██║    ██╔══██╗██╔════╝██╔═══██╗████╗  ██║
██║██║     ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║██████╔╝   ██║   ██║    ██████╔╝██║     ██║   ██║██╔██╗ ██║
██║██║     ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██╗   ██║   ██║    ██╔══██╗██║     ██║   ██║██║╚██╗██║
██║███████╗███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ██║    ██║  ██║╚██████╗╚██████╔╝██║ ╚████║
╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
```

### Illuminati RCON
**Lightweight Remote Monitoring & Management for small teams**

![Version](https://img.shields.io/badge/version-1.4.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/vZQZ8w6zCg)

[Features](#features) • [Quick Start](#quick-start) • [API Reference](#api-reference) • [Windows Service](#windows-service) • [Licensing](#licensing) • [Security](#security-notes)

</div>

---

## Overview

Illuminati RCON is a compact remote monitoring and management (RMM) agent.  
It runs a small FastAPI server on the host machine and optionally a local desktop dashboard. You can check hardware health, launch approved applications, manage IP access lists, lock or shut down the machine, and review an audit trail of privileged actions.

It is designed for **small companies, labs, and technical users** who want something simple rather than a full enterprise RMM suite.

| Mode | Description |
|------|-------------|
| **GUI** | Local CustomTkinter dashboard (first-run setup, live stats, logs, settings) |
| **Headless** | API only — suitable for servers and Windows services |
| **Service** | Installs as a Windows service that starts on boot |

---

## Features

- Cross-platform (Windows, Linux, macOS)
- Live hardware telemetry (CPU, RAM, disk, battery, boot time)
- IP whitelist / blacklist with rate limiting
- Approved application launcher
- Remote lock & shutdown (platform-aware)
- Process termination with protection for critical system processes
- Persistent **audit log** of every privileged action
- Offline license keys (machine-bound)
- Optional TLS (`--ssl-cert` / `--ssl-key`)
- Headless mode and Windows service installer

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run with the GUI (first-time setup)

```bash
python main.py
```

On first launch you will be asked for:
- Admin email
- Admin password (minimum 8 characters)
- API secret key (leave blank to auto-generate)
- Optional license key

### 3. Run headless (no window)

```bash
python main.py --headless --port 8000
```

### 4. Useful flags

```text
--headless          Run API only (no GUI)
--host 0.0.0.0      Bind address (default 0.0.0.0)
--port 8000         Port (default 8000)
--ssl-cert FILE     TLS certificate
--ssl-key FILE      TLS private key
--gen-license NAME  Generate an offline license key and exit
```

---

## Windows Service

The recommended way to run on Windows servers or always-on workstations.

1. Place the product files in a permanent folder (e.g. `C:\RCON\`).
2. Open **PowerShell as Administrator**.
3. Run:

```powershell
cd C:\RCON
pip install -r requirements.txt
.\install_service.ps1
```

The installer uses [NSSM](https://nssm.cc/) (downloaded automatically if needed) and registers a service named **IlluminatiRCON** that starts on boot.

```powershell
# Common commands
nssm start   IlluminatiRCON
nssm stop    IlluminatiRCON
nssm restart IlluminatiRCON
.\uninstall_service.ps1          # clean removal
```

Logs are written next to the script:
- `service_stdout.log` / `service_stderr.log`
- `audit.log` — privileged actions
- `app_visits.log` — every HTTP request

See **INSTALL.md** for full details.

---

## API Reference

The server listens on `0.0.0.0:8000` by default.  
All administrative endpoints require the header:

```http
X-API-Key: <your-api-secret-key>
```

### Public endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Status, version, hostname, license flag |
| GET | `/stats` | CPU, RAM, disk, battery, boot time |
| GET | `/license` | License status (no secrets) |

### Administrative endpoints (API key required)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/open/{alias}` | Launch a registered application |
| GET | `/addwhitelist/{ip}` | Add IP to whitelist |
| GET | `/addblacklist/{ip}` | Add IP to blacklist |
| GET | `/killprocess/{pid}` | Terminate process (refuses critical ones) |
| GET | `/lock` | Lock the workstation |
| GET | `/shutdown?delay=5` | Schedule shutdown |
| GET | `/close` | Exit the RCON process |

**Example**

```bash
curl -H "X-API-Key: YOUR_KEY" http://192.168.1.50:8000/stats
curl -H "X-API-Key: YOUR_KEY" http://192.168.1.50:8000/open/notepad
curl -H "X-API-Key: YOUR_KEY" http://192.168.1.50:8000/lock
```

Rate limit: 60 requests per 60 seconds per IP.

---

## Licensing

Licenses are offline and machine-bound.

**Generate a key (seller side):**

```bash
python main.py --gen-license "Acme Corp"
```

Example output:
```text
IRCON-A1B2C3D4-01-E5F6G7
```

The customer activates the key during first-run setup or later in the **Settings** tab.  
The key is bound to a fingerprint of the machine (hostname + primary MAC). No internet connection is required after activation.

Check status at any time:

```bash
curl http://localhost:8000/license
```

---

## Local GUI

When started without `--headless`, a dark-mode dashboard is shown with these tabs:

| Tab | Purpose |
|-----|---------|
| Dashboard | Live CPU/RAM gauges, host info, lock & exit |
| App Manager | Register application shortcuts, view top processes |
| Network Rules | Whitelist / blacklist, active connections |
| Logs | Request log + privileged audit log |
| Help | API reference with the current (masked) key |
| Settings | Toggle whitelist, rotate API key, activate license |

Guest mode shows limited information; full control requires administrator login.

---

## Security Notes

- Prefer running behind a reverse proxy (nginx / Caddy) with HTTPS.
- Or start with built-in TLS: `--ssl-cert fullchain.pem --ssl-key privkey.pem`.
- Keep the API key secret and rotate it from Settings when needed.
- Enable the IP whitelist and add only trusted management addresses.
- Review `audit.log` periodically.
- Do not expose port 8000 directly to the public internet.
- Critical system processes are refused by the kill-process endpoint.

---

## Files created at runtime

| File | Purpose |
|------|---------|
| `config.json` | Admin credentials, API key, whitelist flag |
| `license.json` | Activated license + machine fingerprint |
| `whitelist.json` / `blacklist.json` | Access control lists |
| `allowed_apps.json` | Application shortcuts |
| `audit.log` | Privileged action trail |
| `app_visits.log` | HTTP request log |

---

## Project layout (distribution)

```text
IlluminatiRCON/
├── main.py                 # Application
├── requirements.txt        # Python dependencies
├── install_service.ps1     # Windows service installer
├── uninstall_service.ps1   # Service removal
├── run_headless.bat        # Quick headless launch (Windows)
├── INSTALL.md              # Detailed install guide
└── README.md               # This file
```

---

## Requirements

- Python 3.10 or newer
- See `requirements.txt` for packages (`fastapi`, `uvicorn`, `psutil`, `customtkinter`, `colorama`, …)

---

## Disclaimer

This software is intended for authorized remote administration of machines you own or manage with explicit permission.  
Unauthorized access to computer systems is illegal. Use responsibly.

---

<div align="center">

**Illuminati RCON** · v1.4.0  
Created by CrazyK  
[Discord](https://discord.gg/vZQZ8w6zCg)

</div>
