<div align="center">

```text
  ██╗██╗░░░░░██╗░░░░░██╗░░░██╗███╗░░███╗██╗███╗░░██╗░█████╗░████████╗██╗░██████╗░██████╗░███╗░░██╗
  ██║██║░░░░░██║░░░░░██║░░░██║████╗████║██║████╗░██║██╔══██╗╚══██╔══╝██║██╔═══██╗██╔══██╗████╗░██║
  ██║██║░░░░░██║░░░░░██║░░░██║██╔████╔██║██║██╔██╗██║███████║░░░██║░░░██║██║░░░██║██████╔╝██╔██╗██║
  ██║██║░░░░░██║░░░░░██║░░░██║██║╚██╔╝██║██║██║╚████║██╔══██║░░░██║░░░██║██║░░░██║██╔══██╗██║╚████║
  ██║███████╗███████╗╚██████╔╝██║░╚═╝░██║██║██║░╚███║██║░░██║░░░██║░░░██║╚██████╔╝██║░░██║██║░╚███║
  ╚═╝╚══════╝╚══════╝░╚═════╝░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝
```

### **Illuminati RCON (Demo Edition)**
*A dual-interface remote administration utility featuring CustomTkinter GUI & FastAPI background architecture.*

---

![Version](https://img.shields.io/badge/version-1.0.0--demo-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Security](https://img.shields.io/badge/security-PyArmor%20Protected-red?style=for-the-badge)

[System Architecture](#system-architecture) • [Core Capabilities](#core-capabilities) • [API Documentation](#api-documentation) • [Installation & Deployment](#installation--deployment)

---

</div>

## System Architecture

**Illuminati RCON** is designed as a hybrid administration platform. It bridges standard desktop operations with network-level HTTP remote management. 

```
┌────────────────────────────────────────────────────────────────────────┐
│                          HOST MACHINE (WINDOWS)                        │
│                                                                        │
│   ┌───────────────────────────┐      ┌─────────────────────────────┐   │
│   │   CustomTkinter GUI       │      │   FastAPI Web Engine        │   │
│   │  (Local Control Panel)    │      │  (Uvicorn / Port 8000)      │   │
│   └─────────────┬─────────────┘      └──────────────┬──────────────┘   │
│                 │                                   │                  │
│                 └───────────────┬───────────────────┘                  │
│                                 ▼                                      │
│                  ┌──────────────────────────────┐                      │
│                  │  Access Control & Middleware │                      │
│                  │  (IP Whitelist/Blacklist Logic)│                      │
│                  └──────────────┬───────────────┘                      │
└─────────────────────────────────┼──────────────────────────────────────┘
                                  ▼
                   ┌──────────────────────────────┐
                   │   Remote Client / Browser    │
                   └──────────────────────────────┘
```

The system initializes by verifying host permissions via remote authentication Gists. Once validated, it spawns an asynchronous Uvicorn server in a dedicated thread while delivering a desktop interface powered by CustomTkinter.

---

## Core Capabilities

* **Real-time Telemetry Processing:** Monitors host hardware metrics including CPU utilization, RAM availability, and battery status via `psutil`.
* **Remote Display Capture:** On-demand desktop screenshots captured at the OS level and streamed back over the HTTP tunnel as raw PNG binaries.
* **Process Execution Engine:** Isolated background process spawning via `subprocess.Popen` for whitelisted applications (Notepad, Task Manager, Calculator, etc.).
* **Dynamic Access Control:** Middleware-level IP filtering supporting real-time whitelisting and blacklisting backed by persistent JSON storage.
* **Tiered Authentication:** Multi-stage privilege escalation system featuring Guest access and Admin verification with `.env` variable mapping.
* **System Power Management:** Remote workstation locking (`ctypes`) and automated shutdown sequences.

---

## Installation & Deployment

### Option A: Standalone Executable Deployment

For end-users running the pre-compiled binary (`illuminati_rcon.exe`):

1. **Prerequisites:** Ensure the target host machine has an active internet connection (required for initial remote handshake and asset fetching).
2. **Directory Setup:** Place `illuminati_rcon.exe` in your desired directory.
3. **Admin Configuration (Optional):** To enable Admin mode, create a `.env` file in the **same directory** as the `.exe` file using the template below:

```env
KEY1=your_console_key_1
KEY2=your_console_key_2
KEY3=your_api_security_key
PASSWORD=your_admin_password
EMAIL=your_registered_email@example.com
```

4. **Launch:** Double-click `illuminati_rcon.exe`. If prompted by Windows Defender, select **"Run anyway"** (heuristic flag caused by PyArmor compilation).

---

### Option B: Running from Source

```bash
# 1. Clone the repository
git clone https://github.com/your-username/illuminati-rcon.git
cd illuminati-rcon

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env

# 4. Run the application
python main.py
```

---

## API Documentation

When the background server initializes, endpoints become accessible via `http://<HOST_IP>:8000`.

### System & Health

```http
GET /
```
Returns overall API status, target device hostname, and current privileges.

```http
GET /stats
```
Retrieves real-time system metrics:

```json
{
  "server_status": "active",
  "hardware_metrics": {
    "cpu_utilization": "12.4%",
    "ram_utilization_percent": "44.1%",
    "ram_available_gigabytes": "8.92 GB"
  },
  "power_metrics": {
    "battery_level": "98%",
    "charging_state": true
  }
}
```

```http
GET /screenshot
```
Captures the host display and returns an `image/png` response.

---

### Remote Control & Process Execution

```http
GET /open/{app_name}
```
Spawns a whitelisted background process. Supported applications: `notepad`, `calculator`, `cmd`, `taskmanager`, `browser`, `spotify`.

```http
GET /lock
```
Triggers `LockWorkStation()` via OS kernel libraries.

```http
GET /shutdown
```
Initiates system shutdown *(Requires Admin Privilege)*.

---

### Access Management

```http
GET /addwhitelist/{key}/{ip}
```
Appends the target IP address to the active whitelist.

```http
GET /addblacklist/{key}/{ip}
```
Appends the target IP address to the active blacklist *(Requires Admin Privilege)*.

---

## Project Structure

```text
├── main.py                # Main application source code
├── .env                   # Environment variable definitions (User-provided)
├── whitelist.json         # Persisted IP whitelist storage
├── blacklist.json         # Persisted IP blacklist storage
├── visits.log             # Network request access log
└── dist/
    └── illuminati_rcon.exe # Single-file executable distribution
```

---

<div align="center">

**Created by CrazyK**  
*For educational and demonstration purposes.*

</div>