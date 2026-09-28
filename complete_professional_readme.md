<div align="center">

```text
  ██╗██╗     ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗██████╗ ████████╗██╗    ██████╗  ██████╗ ███╗   ██╗
  ██║██║     ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██║    ██╔══██╗██╔═══██╗████╗  ██║
  ██║██║     ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║██████╔╝   ██║   ██║    ██████╔╝██║   ██║██╔██╗ ██║
  ██║██║     ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██╗   ██║   ██║    ██╔══██╗██║   ██║██║╚██╗██║
  ██║███████╗███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ██║    ██║  ██║╚██████╔╝██║ ╚████║
  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
```

### **Illuminati RCON: Enterprise-Grade Remote Administration Infrastructure**
*An Asynchronous, Dual-Threaded Remote Orchestration & Hardware Telemetry Engine*

---

![Version](https://img.shields.io/badge/version-1.0.0--ENTERPRISE__DEMO-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Windows_10%2F11-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Obfuscation](https://img.shields.io/badge/obfuscation-PyArmor_8-red?style=for-the-badge)
![Build](https://img.shields.io/badge/packer-PyInstaller_OneFile-orange?style=for-the-badge)

[System Architecture](#-system-architecture--threading-model) • [Security & Auth Protocol](#-security--authentication-protocol) • [Complete API Specification](#-complete-api-specification) • [Local GUI & Controls](#-local-gui--cli-controls) • [Deployment Guide](#-standalone-exe-deployment-guide)

---

</div>

## 🌐 System Architecture & Threading Model

**Illuminati RCON** operates on a non-blocking, multi-threaded hybrid architecture designed to decouple system management tasks from the local graphical application loop.

```text
                                  ┌──────────────────────────────────────────────────────────┐
                                  │                REMOTE NETWORK CLIENT                     │
                                  └────────────────────────────┬─────────────────────────────┘
                                                               │ HTTP / REST Requests (Port 8000)
                                                               ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ HOST MACHINE RUNTIME (ILLUMINATI_RCON.EXE)                                                 │
│                                                                                            │
│   ┌────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ CUSTOM FASTAPI MIDDLEWARE PIPELINE                                                 │   │
│   │                                                                                    │   │
│   │   [Client IP] ──► [Blacklist Check] ──► [Whitelist Check] ──► [Audit Logger]       │   │
│   └─────────────────────────────────────────┬──────────────────────────────────────────┘   │
│                                             │ Passes Verification                          │
│                                             ▼                                              │
│   ┌────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ THREAD 1: ASYNCHRONOUS FASTAPI / UVICORN ENGINE                                    │   │
│   │                                                                                    │   │
│   │   • System Telemetry Telecommunication Engine (/stats)                             │   │
│   │   • Remote Display Screen Capture Tunnel (/screenshot)                             │   │
│   │   • Subprocess Execution Sandbox (/open/{app_name})                                │   │
│   │   • Win32 API Kernel Intercept Routines (/lock, /shutdown)                         │   │
│   └─────────────────────────────────────────┬──────────────────────────────────────────┘   │
│                                             │ Shared State & Memory                        │
│                                             ▼                                              │
│   ┌────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ THREAD 2: MAIN TKLIB / CUSTOMTKINTER GUI LOOP                                      │   │
│   │                                                                                    │   │
│   │   • Native Desktop Control Interface (ctk.CTk)                                     │   │
│   │   • In-Memory Remote Asset Conversion (PNG-to-ICO Engine)                          │   │
│   │   • Console Authentication & Nuclear Sequence Handshake                            │   │
│   └────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                            │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔒 Security & Authentication Protocol

Illuminati RCON utilizes a multi-layered security stack ensuring unauthorized callers cannot manipulate host system operations or snoop on background telemetry:

### 1. Remote Authorization Handshake (Gist Validation)
Upon cold boot, the binary initiates an outgoing HTTPS GET request to a remote JSON configuration Gist (`demo_mode.json`) with an appended cache-busting timestamp parameter (`?cb=epoch_time`).
* **Demo Mode Active:** Bypasses local hostname matching and logs explicit demo notices to standard output.
* **Production Mode Active:** Performs a secondary HTTPS request to pull an `ALLOWEDLIST.json` array containing authorized system hostnames. The local hostname retrieved via `socket.gethostname()` (and its shortened prefix) is matched against the remote whitelist. If unauthorized, execution halts instantly with `sys.exit(1)`.

### 2. Dual-Tier Console Identity Gate
Prior to GUI initialization, the runtime presents an interactive console gate:
* **Guest Tier:** Grants standard read/local access. Disables destructive web routes (`/shutdown`, `/addblacklist`, nuclear triggers).
* **Admin Tier:** Requires matching `EMAIL` and `PASSWORD` definitions stored inside the host `.env` file. Integrated with `email_validator` for deliverability verification and normalized string checking. Includes a persistent failed attempt tracking system (`tries.json`, `login_attempts.json`). Reaching 3 failed attempts forces an immediate application shutdown.

### 3. Middleware Firewalling & Inspection
Every HTTP request routed to the FastAPI web engine passes through an isolated middleware interceptor (`log_all_requests`):
1. **IP Logging:** Captures the origin host IP (`request.client.host`), User-Agent, target URI path, and precise timestamp, writing them sequentially to standard output and `visits.log`.
2. **Blacklist Intercept:** If the origin IP exists within `blacklist.json`, the middleware aborts execution immediately, returning an HTTP 403 Forbidden payload.
3. **Whitelist Intercept:** If `whitelist_enabled` is true and the origin IP is not inside `whitelist.json` (Localhost `127.0.0.1` is permanently pinned), the route returns an HTTP 403 status code.

---

## 🛰 Complete API Specification

The embedded FastAPI server listens on all host network interfaces (`0.0.0.0:8000`). All response payloads are formatted in standard UTF-8 JSON unless otherwise specified.

---

### System Telemetry & Health

#### 1. Server Health Check
* **Endpoint:** `GET /`
* **Access Level:** Public / All Tiers
* **Description:** Verifies that the background FastAPI instance is active and returns target host metadata.
* **Response Payload (200 OK):**
  ```json
  {
    "Status": "Online/200",
    "Message": "Welcome to RCON",
    "Device": "Target device WORKSTATION-PC",
    "Mode": "Admin mode: true"
  }
  ```

#### 2. Network Ping Test
* **Endpoint:** `GET /test`
* **Access Level:** Public / All Tiers
* **Response Payload (200 OK):**
  ```json
  {
    "Test": "this is a test"
  }
  ```

#### 3. Real-Time Hardware Telemetry
* **Endpoint:** `GET /stats`
* **Access Level:** Public / Whitelisted
* **Description:** Queries physical CPU usage over a 100ms sample window via `psutil.cpu_percent()`, evaluates system RAM via `psutil.virtual_memory()`, and polls hardware power supply drivers.
* **Response Payload (200 OK):**
  ```json
  {
    "server_status": "active",
    "hardware_metrics": {
      "cpu_utilization": "14.2%",
      "ram_utilization_percent": "52.8%",
      "ram_available_gigabytes": "7.56 GB"
    },
    "power_metrics": {
      "battery_level": "98%",
      "charging_state": true
    }
  }
  ```

#### 4. Live Desktop Screen Stream
* **Endpoint:** `GET /screenshot`
* **Access Level:** Public / Whitelisted
* **Description:** Triggers an OS-level display screen grab using `PIL.ImageGrab.grab()`, writes the image payload locally to `api_screenshot.png`, and streams the binary raw file back over the HTTP tunnel.
* **Response Headers:** `Content-Type: image/png`
* **Response Payload (500 Internal Server Error):**
  ```json
  {
    "detail": "OS-level display capture failed. Technical Error: <error_string>"
  }
  ```

---

### Remote Control & Application Sandbox

#### 5. Launch Whitelisted Application
* **Endpoint:** `GET /open/{app_name}`
* **Access Level:** Public / Whitelisted
* **Description:** Inspects the `{app_name}` URI parameter against an isolated process dictionary (`ALLOWED_APPLICATIONS`). Spawns the binary asynchronously using `subprocess.Popen` to ensure the web engine never freezes.
* **Supported Apps:** `notepad`, `calculator`, `cmd`, `taskmanager`, `roblox`, `browser`, `pycharm`, `spotify`.
* **Response Payload (200 OK):**
  ```json
  {
    "execution_status": "success",
    "executed_binary": "calc.exe",
    "message": "Successfully spawned process for calculator."
  }
  ```
* **Response Payload (404 Not Found):**
  ```json
  {
    "detail": "Access Denied: Application 'malicious_app' is not registered in the system whitelist."
  }
  ```

#### 6. Remote Workstation Lock
* **Endpoint:** `GET /lock`
* **Access Level:** Public / Whitelisted
* **Description:** Invokes `ctypes.windll.user32.LockWorkStation()`, immediately locking the host machine and returning the Windows user to the login security screen.
* **Response Payload (200 OK):**
  ```json
  {
    "Status": "Success",
    "Message": "Successfully locked"
  }
  ```

#### 7. Remote System Shutdown
* **Endpoint:** `GET /shutdown`
* **Access Level:** **ADMINISTRATOR ONLY**
* **Description:** Executes a shell shutdown directive (`shutdown /s /t 2`) to gracefully terminate host operating system processes within 2 seconds.
* **Response Payload (200 OK):**
  ```json
  {
    "Status": "Success",
    "Message": "Successfully shut down"
  }
  ```
* **Response Payload (200 OK - Blocked):**
  ```json
  {
    "Status": "BLOCKED",
    "Message": "Admin mode disabled."
  }
  ```

#### 8. Asynchronous API Server Termination
* **Endpoint:** `GET /close`
* **Access Level:** Public / Whitelisted
* **Description:** Schedules a background cleanup task (`realcloseapi`) using FastAPI `BackgroundTasks`. Sleep-delivers the 200 OK HTTP packet to the client before executing a forceful Win32 process kill (`taskkill /f /im python.exe`).
* **Response Payload (200 OK):**
  ```json
  {
    "Status": "Success",
    "Message": "Successfully sent close request"
  }
  ```

---

### Network Access Control Routines

#### 9. Append IP to Whitelist
* **Endpoint:** `GET /addwhitelist/{key}/{ip}`
* **Access Level:** Requires Security `KEY3`
* **Description:** Verifies that `{key}` matches `KEY3` from the environment configuration. Appends `{ip}` to `whitelist.json` and updates the active runtime `WHITELIST` set.
* **Response Payload (200 OK):**
  ```json
  {
    "Status": "Success",
    "Message": "192.168.1.150 added to whitelist"
  }
  ```

#### 10. Append IP to Blacklist
* **Endpoint:** `GET /addblacklist/{key}/{ip}`
* **Access Level:** **ADMINISTRATOR ONLY** + Security `KEY3`
* **Description:** Validates admin privileges and security key `KEY3`. Appends `{ip}` to `blacklist.json` and blocks all subsequent HTTP calls originating from that address.
* **Response Payload (200 OK):**
  ```json
  {
    "Status": "Success",
    "Message": "192.168.1.200 added to blacklist"
  }
  ```

---

## 💻 Local GUI & CLI Controls

The desktop interface (`CustomTkinter`) provides direct physical host operations:

* **Lock Workstation:** Immediately triggers kernel desktop locking.
* **System Shutdown:** Opens a native Win32 confirmation dialog (`MessageBoxW`) before executing host power-off.
* **Test API:** Dispatches an internal HTTP request to `http://127.0.0.1:8000` to verify background server responsiveness.
* **IP Management Panel:** Admin-only UI entry forms allowing live addition and removal of IP addresses from `whitelist.json` and `blacklist.json`.
* **Nuclear Verification Routine:** Two-phase console key verification process (`KEY1` & `KEY2`) requiring both terminal key entry and web API verification via `/nuclearsequence/verify/{key}`.

---

## 📦 Standalone EXE Deployment Guide

### Environment Variable Setup (`.env`)
To run the `.exe` in **Admin Mode**, place a `.env` file in the **exact same directory** as `illuminati_rcon.exe`:

```env
KEY1=your_console_key_1
KEY2=your_console_key_2
KEY3=your_api_security_key
PASSWORD=your_admin_password
EMAIL=your_registered_email@example.com
```

### PyArmor & PyInstaller Build Pipeline

To compile the obfuscated binary yourself:

```cmd
pyarmor gen --pack "--onefile" main.py
```

The output executable will be created inside the `dist/` directory as `illuminati_rcon.exe`.

---

<div align="center">

**Created by CrazyK**  
*For educational, research, and authorized remote administration purposes.*

</div>