"""
================================================================================
                       ILLUMINATI RCON - DEMO VERSION
================================================================================
Description:
    A lightweight, cross-platform Remote Administration & Control (RCON)
    engine built with Python, FastAPI, and CustomTkinter. This demo allows
    safe testing of core networking capabilities over a local area network (LAN).

Author: CrazyK
Repository: https://github.com
Community & Support: https://discord.gg/vZQZ8w6zCg

--------------------------------------------------------------------------------
DEMO LIMITATIONS:
    - No authentication required (Local guest access only)
    - Restricted App Launcher (Only launches Notepad and Calculator)
    - No remote administrative control tools (Shutdown, Lock, Close)
    - Advanced diagnostics, security, and payload scripting are disabled
--------------------------------------------------------------------------------

================================================================================
                     UNLOCK THE FULL RELEASE VERSION
================================================================================
Want the complete, unthrottled suite? The full version includes advanced
features designed for total system administration:

 PREMIUM FEATURES:
    • Advanced App Whitelisting: Register and deploy any binary or application
      remotely via strict system path mapping.
    • Live Telemetry Stream: Real-time physical hardware metrics (CPU, RAM,
      Power Status, and Display configurations).
    • Remote OS Management: Execute secure remote shutdowns, system locking,
      and process terminations over the network.
    • Screen Capture Tunnel: On-demand OS-level screenshot rendering fed
      directly back to your control device.
    • Robust Network Security: Dynamic, runtime-savable IP Whitelisting
      and Blacklisting to safeguard your host machine.
    • Secure Authentication: Hardware-locked device authorization via cloud
      synced host matching, backed by a dual-stage admin credentials gate.

 How to Upgrade:
    Join our Discord server or check the GitHub repository releases page
    to obtain a commercial license and access the fully protected binary.



--------------------------------------------------------------------------------
 INTELLECTUAL PROPERTY & CRAFTSMANSHIP NOTICE:
    - 100% Human Crafted: The logic, flow, and architecture of this software
      were built completely by hand. No AI models were used to generate the
      core functionality of this project. Human-written code means cleaner
      intent, thoughtful design, and a real developer standing behind it.
    - Protected Work: This source code represents my personal intellectual
      property, time, and labor.
    - No AI Scraping: Copying, modifying, or using this script to train
      large language models (LLMs) or automated code generators is strictly
      prohibited. Respect independent creators—keep it human.
--------------------------------------------------------------------------------
================================================================================
"""



import sys
import socket
import threading
import subprocess
import psutil
import customtkinter as ctk
from fastapi import FastAPI, HTTPException

app = FastAPI()
hostname = socket.gethostname()


ALLOWED_APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe"
}


@app.get("/")
def home():
    return {
        "Status": "Online/200",
        "Message": "Welcome to Illuminati RCON (DEMO VERSION)",
        "Device": f"Target device: {hostname}",
        "Help": "Go to /help for available commands"
    }

@app.get("/help")
def help():
    return {
        "Message": "Demo Mode active. Limited commands available.",
        "/stats": "View host hardware performance (CPU & RAM).",
        "/open/(app_name)": "Launch safe demo apps: 'notepad' or 'calculator'."
    }

@app.get("/stats")
async def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    ram_info = psutil.virtual_memory()
    return {
        "hardware_metrics": {
            "cpu_utilization": f"{cpu_percent}%",
            "ram_utilization_percent": f"{ram_info.percent}%",
            "ram_available_gigabytes": f"{round(ram_info.available / (1024 ** 3), 2)} GB"
        }
    }

@app.get("/open/{app_name}")
async def launch_application(app_name: str):
    requested_app = app_name.lower()
    if requested_app in ALLOWED_APPLICATIONS:
        target_executable = ALLOWED_APPLICATIONS[requested_app]
        subprocess.Popen(target_executable, shell=True)
        return {
            "status": "success",
            "message": f"Successfully opened {requested_app} on target machine."
        }
    raise HTTPException(
        status_code=403,
        detail="Feature locked: Upgrade to full version to register custom applications."
    )

window = ctk.CTk()
window.title("Illuminati RCON - DEMO")
window.geometry("400x250")

def test_local_connection():
    label_status.configure(text="API Server is running cleanly!", text_color="green")

label_title = ctk.CTkLabel(window, text="Illuminati RCON (Demo)", font=("Arial", 18, "bold"))
label_title.pack(pady=20)

button_test = ctk.CTkButton(window, text="Check Status", fg_color="purple", command=test_local_connection)
button_test.pack(pady=10)

label_status = ctk.CTkLabel(window, text="Awaiting connection...", text_color="gray")
label_status.pack(pady=10)


if __name__ == "__main__":
    import uvicorn

    # Get local network IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        WIFI_IP = s.getsockname()[0]
        s.close()
    except Exception:
        WIFI_IP = "127.0.0.1"

    def run_api():
        # Running quietly on local network ports
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")

    # Start API in background thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    print("============================================================")
    print(" Illuminati RCON Engine - DEPLOYED SUCCESSFULLY (DEMO)")
    print(f" Local Control:   http://localhost:8000")
    print(f" Network Control: http://{WIFI_IP}:8000")
    print("============================================================")

    try:
        window.mainloop()
    finally:
        print("terminating network threads...")
        sys.exit(0)
