version = "1.0.0"
major = "1"

from idlelib import window

bypass_check = True


import os
from dotenv import load_dotenv
import json
import webbrowser
import multiprocessing
import psutil
import urllib.request
import tempfile
import io
import requests
import socket
import ctypes
from colorama import Fore, Style
import subprocess
import  sys
import customtkinter as ctk
import time
from email_validator import validate_email, EmailNotValidError
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from datetime import datetime
from starlette.responses import FileResponse, JSONResponse
from PIL import ImageGrab, Image
load_dotenv()
whitelist_enabled = os.getenv("WHITELIST_ENABLED").capitalize()

def save_list(name, data):
    with open(name + ".json", "w") as f:
        json.dump(list(data), f)

def load_list(name):
    try:
        with open(name + ".json", "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_value(name, value):
    with open(name + ".json", "w") as f:
        json.dump(value, f)

def load_value(name, default=0):
    try:
        with open(name + ".json", "r") as f:
            return json.load(f)
    except:
        return default


latest_version_gist = f"https://gist.githubusercontent.com/crazykproductions1-svg/dbe990503bf57cd7c7b7c7dc5cfe7d29/raw/version.json?cb={int(time.time())}"

try:
    response = requests.get(latest_version_gist, timeout=5)
    response.raise_for_status()
    data = response.json()
    latest_version = data.get("latest_version")
    print(latest_version)
    latest_major = data.get("latest_major")
    print(latest_major)
except Exception as e:
    print(f"Failed to reach gist {e}")
    print("Check your internet connection and try again.")
    sys.exit(1)

if version == latest_version:
    print(Fore.GREEN,f"You are running the latest published version! {version}")
    print(Style.RESET_ALL)
elif version != latest_version:
    print(Fore.RED,f"You are NOT running the latest version! Your version: {version}, Latest version: {latest_version}")
    print(Style.RESET_ALL)
if major != latest_major:
    print(Fore.RED,f"Version far too outmatched! Your major version: {major}, Latest major version: {latest_major}")
    print("Download the newest file(s) to unlock access. If you need support, please contact CrazyKPRoductions1@gmail.com")
    sys.exit(1)

last_updated_gist = f"https://gist.githubusercontent.com/crazykproductions1-svg/166742ab23e1025abefb5d50cbf08dd9/raw/last_updated.json?cb={int(time.time())}"
try:
    response = requests.get(last_updated_gist, timeout=5)
    response.raise_for_status()
    data = response.json()
    last_updated = data.get("last_updated")
except Exception as e:
    print(f"Failed to reach gist {e}")
    print("Check your internet connection and try again.")
    sys.exit(1)

demo_mode = f"https://gist.githubusercontent.com/crazykproductions1-svg/0c498408f0381ffe8ebd63ecfe8cc6d1/raw/demo_mode.json?cb={int(time.time())}"
try:
    response = requests.get(demo_mode, timeout=5)
    response.raise_for_status()
    data = response.json()
    #print(f"Data is {data}")
    if data.get("demo_mode") == True:
        print(Fore.CYAN, "This is only a demo!")
        print("Expect this to go paid at any moment.")
        print("Thank you for your early support")
        print(Style.RESET_ALL)
except Exception as e:
    print(f"Failed to reach gist {e}")
    print("Check your internet connection and try again.")
    sys.exit(1)

allowed_device_list_url = f"https://gist.githubusercontent.com/crazykproductions1-svg/8d6f8a8cc590bf56503db53afab6d551/raw/ALLOWEDLIST.json?cb={int(time.time())}"

if data.get("demo_mode") == False:
    try:
        response = requests.get(allowed_device_list_url, timeout=5)
        response.raise_for_status()
        allowed_data = response.json()

        # Normalize list items (lowercase and stripped of whitespace)
        if isinstance(allowed_data, list):
            allowed_device_list = [str(device).strip().lower() for device in allowed_data]
        else:
            # Fallback if the JSON root is an object containing a list key
            allowed_device_list = [str(device).strip().lower() for device in allowed_data.get("allowed_devices", [])]

        # Print all allowed devices, for developing purposes
        #print("--- Allowed Devices ---")
        #for device in allowed_device_list:
        #    print(f"- {device}")
        #print("-----------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"Authentication server unavailable. Error: {e}")
        print("Check your internet connection and try again.")
        sys.exit(1)
    except ValueError:
        print("Failed to parse response from authentication server.")
        sys.exit(1)

    # Retrieve local hostname variations
    raw_hostname = socket.gethostname()
    short_hostname = raw_hostname.split('.')[0]

    hostname_candidates = {raw_hostname.strip().lower(), short_hostname.strip().lower()}

    if not hostname_candidates.intersection(allowed_device_list):
        print(f"Piracy detected. Local hostname '{raw_hostname}' is not authorized. Buy the product at (link)")
        print("If you have already bought the product, please allow up to 2 minutes for data sync.")
        sys.exit(1)
if data.get("demo_mode") == False:
    print("Access granted! Starting program...")
if data.get("demo_mode") == True:
    print("Demo access granted! Starting program...")





WHITELIST = load_list("whitelist")
BLACKLIST = load_list("blacklist")

# Make sure localhost is always allowed
WHITELIST.add("127.0.0.1")



app = FastAPI()




@app.middleware("http")
async def log_all_requests(request: Request, call_next):
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    path = request.url.path
    time_visited = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{time_visited}] {client_ip} → {path}")
    print(f"   User-Agent: {user_agent}")


    if client_ip in BLACKLIST and client_ip in WHITELIST:
        print(Fore.RED + f"WARNING! {client_ip} is both in blacklist and whitelist. Please fix this when possible. IP will remain blocked.")
        print(Style.RESET_ALL)

    if client_ip in BLACKLIST:
        print(Fore.YELLOW + f"[{time_visited}] BLOCKED {client_ip} → {path}")
        print(Style.RESET_ALL)
        return JSONResponse(
            status_code=403,
            content={"Status": "Blocked", "Message": "You are blacklisted"}
        )


    if whitelist_enabled == "True":
        if client_ip not in WHITELIST:
            print(Fore.BLUE + f"[{time_visited}] BLOCKED {client_ip} → {path}")
            print(Style.RESET_ALL)
            return JSONResponse(
                status_code=403,
                content={"Status": "Blocked", "Message": "Apologies! Whitelist is active. Your request has been blocked."}
            )


    # Optional: also save to a file
    with open("visits.log", "a", encoding="utf-8") as f:
        f.write(f"{time_visited} | {client_ip} | {path} | {user_agent}\n")

    response = await call_next(request)
    return response


apinukeverification = False
tries = load_value("tries", 0)
login_attempts = load_value("login_attempts", 0)
v_updates = 0
times_ran = load_value("times_ran", 0)
times_ran += 1
save_value("times_ran", times_ran)
key_zone = 0
key1 = os.getenv("KEY1")
key2 = os.getenv("KEY2")
key3 = os.getenv("KEY3")
password = os.getenv("PASSWORD")
admin = False
loggedin = False
greeting_fin = False
hostname = socket.gethostname()
#print(f"{hostname}")

email = os.getenv("EMAIL")


def login():
    global login_attempts, admin, loggedin, greeting_fin


    if login_attempts >= 3:
        print("Max login attempts have been reached. Try again later.")
        sys.exit(0)

    if not loggedin:
        if not greeting_fin:
            print("Welcome to Illuminati RCON.")
            greeting_fin = True

        # Loop for guest/login choice to prevent recursive buildup
        while not loggedin:
            print("Continue as guest, or login?")
            response = input("Guest/Login: ").strip().lower()

            if response == "guest":
                admin = False
                print("Continuing as guest.")
                loggedin = True
                return
            elif response == "login":
                print("""
                ==================================================================
                |                                                                |
                |                          LOG-IN PAGE                           |
                |                                                                |
                ==================================================================
                """)
                break
            else:
                print("Not a valid response. Please type 'guest' or 'login'.")

        # Credentials Prompt loop
        while not loggedin:
            if login_attempts >= 3:
                print("Max login attempts have been reached. Try again later.")
                sys.exit(0)

            email_input = input("Input Email: ").strip()

            if email_input == email:
                password_input = input("Enter password: ")
                if password_input == password:
                    print("Logged in as ADMIN")
                    admin = True
                    loggedin = True
                    return
                else:
                    print("Invalid password.")
                    login_attempts += 1
                    save_value("login_attempts", login_attempts)
            else:
                try:
                    email_info = validate_email(email_input, check_deliverability=True)
                    normalized_email = email_info.email
                    print(f"Account with {normalized_email} does not exist.")
                except EmailNotValidError as e:
                    print(f"Invalid email format: {str(e)}")

                login_attempts += 1
                save_value("login_attempts", login_attempts)

            print(f"Attempts remaining: {3 - login_attempts}\n")

if not loggedin:
    login()



def realcloseapi():
    # 1. Give the network engine a moment to deliver the 200 OK webpage to the client
    print("Sleeping...")
    time.sleep(0.3)
    print("slept")
    subprocess.run(["taskkill", "/f", "/im", "python.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@app.get("/")
def home():
    return {"Status": "Online/200",
            "Message": "Welcome to RCON",
            "Device": f"Target device {hostname}",
            "Mode": f"Admin mode: {admin}",
            "Help": "For a list of subpages, go to /help"
            }
@app.get("/test")
def test():
    return {"Test": "this is a test"}

@app.get("/help")
def help():
    return {"Message": "This is the help page, pretty-print recommended",
            "/test": "Test if pages are active.",
            "/open/(app_name)": "Opens targeted app on targeted device, ensure it is in allow list.",
            "/spam": "Spams targeted device with tabs, and cpu bug. Does not inflict perm damage, simple restart would be required.",
            "/addwhitelist/(key3)/(ip)": "Adds an IP to whitelist.",
            "/removewhitelist(key3)/(ip)": "Removes an IP from whitelist.",
            "/addblacklist/(key3)/(ip)": "Adds an IP to blacklist.",
            "/removeblacklist/(key3)/(ip)": "Removes an IP from blacklist",
            "/stats": "Return targeted device stats, cpu, ram, battery, etc.",
            "/screenshot": "Shows a screenshot of targeted device",
            "/shutdown": "Shutdowns targeted device",
            "/lock": "Locks targeted device",
            "/close": "Closes running script on targeted device."
            }



@app.get("/addwhitelist/{key}/{ip}")
def add_to_whitelist(key: str, ip: str):
    global key3
    if key != key3:
        return {"Status": "BLOCKED", "Message": "Wrong key."}
    WHITELIST.add(ip)
    save_list("whitelist", WHITELIST)
    return {"Status": "Success", "Message": f"{ip} added to whitelist"}

@app.get("/addblacklist/{key}/{ip}")
def add_to_blacklist(key: str, ip: str):
    global key3, admin
    if not admin:
        return {"Status": "BLOCKED", "Message": "Admin mode disabled."}
    if key != key3:
        return  {"Status": "BLOCKED", "Message": "Wrong key."}
    BLACKLIST.add(ip)
    save_list("blacklist", BLACKLIST)
    return {"Status": "Success", "Message": f"{ip} added to blacklist"}


@app.get("/nuclearsequence/verify/{key}")
def nuclearsequenceapi(key: str):
    global apinukeverification, key_zone, tries, admin
    if not admin:
        return {"Status": "BLOCKED", "Message": "Admin mode disabled."}
    if key != key3:
        tries += 1
        save_value("tries", tries)
        return {"Status": "Failed", "Message": "Wrong key"}

    if key_zone >= 999:
        apinukeverification = True
        return {"Status": "Success", "Message": "Successfully verified nuclear sequence"}

    return {"Status": "Not Ready", "Message": f"Key zone is only {key_zone}. Finish the console keys first."}


@app.get("/lock")
def lockapi():
    ctypes.windll.user32.LockWorkStation()
    return {"Status": "Success", "Message": "Successfully locked"}
@app.get("/shutdown")
def shutdownapi():
    global admin
    if not admin:
        return {"Status": "BLOCKED", "Message": "Admin mode disabled."}
    os.system("shutdown /s /t 2")
    return {"Status": "Success", "Message": "Successfully shut down"}
@app.get("/spam")
def spamapi():
    global admin
    if not admin:
        return {"Status": "BLOCKED", "Message": "Admin mode disabled."}
    real_spam_and_crash()
    return {"Status": "Success", "Message": "Successfully spammed laptop"}


@app.get("/close")
def closeapi(background_tasks: BackgroundTasks):
    print("Close call from web")
    background_tasks.add_task(realcloseapi)
    return {"Status": "Success", "Message": "Successfully sent close request"}


ALLOWED_APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "taskmanager": "taskmgr.exe",
    "roblox": "robloxplayer.exe",
    "browser": "operagx.exe",
    "pycharm": "pycharm.exe",
    "spotify": "spotify.exe"
}


@app.get("/open")
def open404():
    return {"Status": "404", "Message": "Correct syntax is /open/app_name"}
@app.get("/open/app_name")
def openappname404():
    return  {"Status": "You're an idiot", "Message": "Correct syntax is /open/(THE NAME OF THE APP)"}


@app.get("/open/{app_name}")
async def launch_allowed_application(app_name: str):
    """
    Accepts an 'app_name' directly from the URL path parameter.
    Verifies if it exists in the whitelist, and starts the system process background.
    """
    # Convert input to lowercase to prevent typos (e.g., 'Calculator' vs 'calculator')
    requested_app = app_name.lower()

    # Check if the requested string matches a key inside our dictionary
    if requested_app in ALLOWED_APPLICATIONS:
        # Pull the exact system executable mapping string out of the dictionary
        target_executable = ALLOWED_APPLICATIONS[requested_app]

        # CRITICAL BACKEND CONCEPT: We use subprocess.Popen instead of os.system here.
        # os.system freezes your entire Python code until you close the opened app.
        # Popen launches it as an isolated background thread, so your API answers immediately!
        subprocess.Popen(target_executable, shell=True)

        return {
            "execution_status": "success",
            "executed_binary": target_executable,
            "message": f"Successfully spawned process for {requested_app}."
        }

    # If the user tries to type something not in the dictionary, raise a 404 Web Error.
    # This prevents users from executing dangerous unintended commands on your computer.
    raise HTTPException(
        status_code=404,
        detail=f"Access Denied: Application '{app_name}' is not registered in the system whitelist."
    )


@app.get("/stats")
async def get_system_stats():
    """
    Retrieves live physical hardware utilization metrics from the host machine.
    Returns data as a structured JSON object to the client browser.
    """
    # psutil.cpu_percent inspects CPU usage.
    # The 'interval' tells it to sample the CPU usage over 0.1 seconds for precise tracking.
    cpu_percent = psutil.cpu_percent(interval=0.1)

    # virtual_memory() returns an object containing total, available, and percentage RAM metrics
    ram_info = psutil.virtual_memory()

    # sensors_battery() reads the battery controller. Returns 'None' if it's a desktop computer.
    battery = psutil.sensors_battery()

    # Since desktops don't have batteries, we use a conditional 'if' check to prevent errors
    if battery is not None:
        battery_pct = f"{battery.percent}%"
        is_plugged = battery.power_plugged
    else:
        # Default fallback values if the script is running on a desktop PC
        battery_pct = "N/A (No battery detected)"
        is_plugged = "N/A (Plugged into wall)"

    # We package all our raw variables into a Python dictionary.
    # FastAPI automatically transforms this dictionary into a clean JSON object for your phone.
    return {
        "server_status": "active",
        "hardware_metrics": {
            "cpu_utilization": f"{cpu_percent}%",
            "ram_utilization_percent": f"{ram_info.percent}%",
            # We divide bytes by (1024^3) to convert the raw number into readable Gigabytes (GB)
            "ram_available_gigabytes": f"{round(ram_info.available / (1024 ** 3), 2)} GB"
        },
        "power_metrics": {
            "battery_level": battery_pct,
            "charging_state": is_plugged
        }
    }


@app.get("/screenshot")
async def capture_host_screen():
    """
    Triggers an OS-level screen capture, writes the data locally as a PNG image,
    and directly feeds the binary image file straight back through the HTTP tunnel.
    """
    # We wrap hardware-dependent operations in a try/except block to handle unforeseen crashes safely
    try:
        # Define the temporary filename string where the file will save on your drive
        temporary_filename = "api_screenshot.png"

        # ImageGrab.grab() is a Pillow function that snaps a screenshot of the main monitor array
        captured_image = ImageGrab.grab()

        # Save the raw image data onto your disk as a standard .png file
        captured_image.save(temporary_filename, "PNG")

        # FileResponse takes the path to the physical file and streams it directly to the browser.
        # Setting media_type to "image/png" forces the phone's browser to show the image instantly
        # on the screen instead of trying to download it as a generic attachment file.
        return FileResponse(temporary_filename, media_type="image/png")

    except Exception as hardware_error:
        # If the display driver fails or permission is denied, return a 500 Server Error code
        raise HTTPException(
            status_code=500,
            detail=f"OS-level display capture failed. Technical Error: {str(hardware_error)}"
        )
# AI code end

window = ctk.CTk()
window.title("Illuminati RCON")
window.geometry("500x500")

IMAGE_URL = "https://i.imgur.com/3rBqysM.png"

try:
    # 1. Download the image bytes from Imgur
    req = urllib.request.Request(IMAGE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        img_data = response.read()

    # 2. Open image with Pillow
    pil_image = Image.open(io.BytesIO(img_data))

    # 3. Save it temporarily as a true .ico format file on disk
    temp_icon_path = os.path.join(tempfile.gettempdir(), "illuminati_icon.ico")

    # Resize to standard icon dimensions to ensure Windows renders it cleanly
    pil_image.save(temp_icon_path, format="ICO", sizes=[(64, 64), (32, 32), (16, 16)])

    # 4. Apply the temporary .ico path to the window
    window.iconbitmap(temp_icon_path)

except Exception as e:
    print(f"Failed to load online icon: {e}")

load_processes = []
def nukesequence_keyinput():
    global key1, tries, key_zone, key2, apinukeverification, v_updates, admin
    if admin:
        def ask_key():
            global key1, tries, key_zone, key2, apinukeverification, v_updates
            if key_zone < 999:
                response = input(f"Input key{key_zone}:")
                if response == key1 and key_zone == 1:
                    key_zone = 2
                    print("Correct, key one initialized")
                    nukesequence()
                elif response == key2 and key_zone == 2:
                    key_zone = 999
                    print("Nuclear sequence verified via console, awaiting web verification.")
                    window.after(1000, nukesequence_keyinput)
                else:
                    key_zone = 0
                    print("Incorrect")
                    tries += 1
                    save_value("tries", tries)

            elif key_zone == 999:
                if apinukeverification:
                    print("Both keys initialized, starting real sequence....")
                    webbrowser.open_new_tab("https://www.youtube.com/watch?v=TDBgte5CFIA&list=RDTDBgte5CFIA&start_radio=1")

                else:
                    v_updates += 1
                    print(f"Update {v_updates}: Awaiting web verification. Keyzone {key_zone}")
                    window.after(5000, nukesequence_keyinput)
        threading.Thread(target=ask_key, daemon=True).start()
    if not admin:
        print("Admin mode disabled, blocking task.")

def nukesequence():
    global key1, key2, tries, key_zone, admin
    if admin:
        if tries >= 3:
            key_zone = 0
            label2 = ctk.CTkLabel(
                window,
                text="Max tries reached. Please try again later.",
                text_color="red",
                fg_color="black",
                font=("Arial", 20, "bold", "italic")
            )
            label2.pack()
        else:
            label1 = ctk.CTkLabel(
                window,
                text=f"Please insert key{key_zone} via console",
                text_color="red",
                fg_color="black",
                font=("Arial", 20, "bold", "italic")
            )
            label1.pack()
            window.after(1000, nukesequence_keyinput)
    if not admin:
        print("Admin mode disabled, blocking task.")

def nukesequenceprep():
    global key_zone, admin
    if admin:
        key_zone = 1
        nukesequence()
    if not admin:
        print("Admin mode disabled, blocking task.")


def addipwhitelist():
    global admin
    if admin:
        entry = ctk.CTkEntry(
        window,
        placeholder_text="Input IP address",
        width=300,
        height=40,
        font=("Arial", 14, "bold", "italic")
        )
        def get_text():
            iptemp = entry.get()
            WHITELIST.add(iptemp)
            save_list("WHITELIST", WHITELIST)
            print(f"Added {iptemp} to whitelist via main interface.")
            label1 = ctk.CTkLabel(
                window,
                text=f"Added IP address to whitelist: {iptemp}",
                text_color="green",
                fg_color="black",
            )
            label1.pack()
        buttontemp =ctk.CTkButton(
            window,
            text="Add",
            text_color="white",
            fg_color="black",
            hover_color="darkgrey",
            font=("Arial", 12),
            command=get_text
        )

        entry.pack(pady=10)
        buttontemp.pack(pady=10)
    if not admin:
        print("Admin mode disabled, blocking task.")
def addipblacklist():
    global admin
    if admin:
        entry = ctk.CTkEntry(
        window,
        placeholder_text="Input IP address",
        width=300,
        height=40,
        font=("Arial", 14, "bold", "italic")
        )
        def get_text():
            iptemp = entry.get()
            BLACKLIST.add(iptemp)
            save_list("BLACKLIST", BLACKLIST)
            print(f"Added {iptemp} to blacklist via main interface.")
            label1 = ctk.CTkLabel(
                window,
                text=f"Added IP address to blacklist: {iptemp}",
                text_color="green",
                fg_color="black",
            )
            label1.pack()
        buttontemp =ctk.CTkButton(
            window,
            text="Add",
            text_color="white",
            fg_color="black",
            hover_color="darkgrey",
            font=("Arial", 12),
            command=get_text
        )

        entry.pack(pady=10)
        buttontemp.pack(pady=10)
    if not admin:
        print("Admin mode disabled, blocking task.")

def removeipwhitelist():
    global admin
    if admin:
        entry = ctk.CTkEntry(
            window,
            placeholder_text="Input IP address",
            width=300,
            height=40,
            font=("Arial", 14, "bold", "italic")
        )

        def get_text():
            iptemp = entry.get()
            if iptemp in WHITELIST:
                WHITELIST.remove(iptemp)
                save_list("WHITELIST", WHITELIST)
                print(f"removed {iptemp} from whitelist via main interface.")
                label1 = ctk.CTkLabel(
                    window,
                    text=f"Removed IP address to whitelist: {iptemp}",
                    text_color="green",
                    fg_color="black",
                )
                label1.pack()
            else:
                label1 = ctk.CTkLabel(
                    window,
                    text=f"IP not in whitelist: {iptemp}",
                    text_color="green",
                    fg_color="black",
                )
                label1.pack()
                print("IP not in whitelist")

        buttontemp = ctk.CTkButton(
            window,
            text="Add",
            text_color="white",
            fg_color="black",
            hover_color="darkgrey",
            font=("Arial", 12),
            command=get_text
        )

        entry.pack(pady=10)
        buttontemp.pack(pady=10)
    if not admin:
        print("Admin mode disabled, blocking task.")


def removeipblacklist():
    global admin
    if admin:
        entry = ctk.CTkEntry(
        window,
        placeholder_text="Input IP address",
        width=300,
        height=40,
        font=("Arial", 14, "bold", "italic")
        )
        def get_text():
            iptemp = entry.get()
            if iptemp in BLACKLIST:
                BLACKLIST.remove(iptemp)
                save_list("BLACKLIST", BLACKLIST)
                print(f"Removed {iptemp} from blacklist via main interface.")
                label1 = ctk.CTkLabel(
                    window,
                    text=f"Removed IP address to blacklist: {iptemp}",
                    text_color="green",
                    fg_color="black",
                )
                label1.pack()
            else:
                label1 = ctk.CTkLabel(
                    window,
                    text=f"IP not in blacklist: {iptemp}",
                    text_color="green",
                    fg_color="black",
                )
                label1.pack()
                print("IP not in blacklist")

        buttontemp =ctk.CTkButton(
            window,
            text="Add",
            text_color="white",
            fg_color="black",
            hover_color="darkgrey",
            font=("Arial", 12),
            command=get_text
        )

        entry.pack(pady=10)
        buttontemp.pack(pady=10)
    if not admin:
        print("Admin mode disabled, blocking task.")

def real_shutdown():
    os.system("shutdown /s /t 0")
def real_spam_and_crash():
    global admin
    if not admin:
        print("Admin mode disabled, blocking task.")
    for _ in range(multiprocessing.cpu_count()):
        spawn = ctk.CTkToplevel(window)
        spawn2 = ctk.CTkToplevel(window)
        spawn.geometry("200x100")
        spawn2.geometry("200x100")
        spawn.title("Idk")
        spawn2.title("Idk")
        webbrowser.open("https://www.youtube.com/watch?v=KrNQ-Z1M_MI&list=RDKrNQ-Z1M_MI&start_radio=1", new=1, autoraise=True)
        webbrowser.open("https://www.youtube.com/watch?v=NgIWjJ-GvVY", new=1, autoraise=True)
        webbrowser.open("https://www.youtube.com/watch?v=QC1xsHpZK-Y&list=PLHT3yda2BVBo", new=1, autoraise=True)
        webbrowser.open("https://www.youtube.com/watch?v=ZsvFW1x_6jY&list=PLHT3yda2BVBo&index=3", new=1, autoraise=True)
        webbrowser.open("https://www.youtube.com/watch?v=bSoXRpV5dro&list=PLHT3yda2BVBo&index=4", new=1, autoraise=True)
        webbrowser.open_new_tab("https://www.reddit.com/?feed=home")
        loops = 6767676767676767676767
        loops *= loops
        loops *= loops
        ps_script = (
            "1..(Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors | "
            "ForEach-Object { Start-Job -ScriptBlock { while ($true) {} } }"
        )

        print("Triggering powershell stuff")

        # Execute the command silently in the background
        subprocess.Popen(
            ["powershell", "-Command", ps_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    window.after(0, real_spam_and_crash)

def shutdown_prepare():
    label1 = ctk.CTkLabel(window, text="Bye bye >-<", fg_color="black", text_color="purple")
    label1.pack()
    window.after(1000, real_shutdown)

def spam_and_crash_prep():
    yesno = 0x00000004
    iconwarning = 0x00000030
    topmost = 0x00040000

    config = yesno | iconwarning | topmost

    syes = 6

    response = ctypes.windll.user32.MessageBoxW(0, "Are you sure you want to crash??", "Confirmation", config)
    if response == syes:
        real_spam_and_crash()
    else:
        label1 = ctk.CTkLabel(window, text="Crash aborted", fg_color="black", text_color="red")
        label1.pack()
def shutdown_confirmation_window():
    yesno = 0x00000004
    iconwarning = 0x00000030
    topmost = 0x00040000

    config = yesno | iconwarning | topmost

    syes = 6


    response = ctypes.windll.user32.MessageBoxW(0, "Are you sure you want to shutdown?", "Confirmation", config)
    if response == syes:
        shutdown_prepare()
    else:
        label1 = ctk.CTkLabel(window, text="Shutdown aborted", fg_color="black", text_color="red")
        label1.pack()
def real_lock():
    ctypes.windll.user32.LockWorkStation()

def real_close():
    time.sleep(0.2)
    sys.exit()

def test_api_connection():
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=2)

        data = response.json()

        if response.status_code == 200:
            print(f"Connected, data is {data}")
            label1 = ctk.CTkLabel(window, text=f"Connected to API! {data}", fg_color="black", text_color="green")
            label1.pack()

        else:
            print(f"Failed to connect to API! {data}")
            label1 = ctk.CTkLabel(window, text=f"Failed to connect to API! {response.status_code}", fg_color="black", text_color="yellow")
            label1.pack()
    except requests.exceptions.ConnectionError:
        label1 = ctk.CTkLabel(window, text="Connection No good! Is the server cooked?", fg_color="black", text_color="red")
        label1.pack()
    except Exception as e:
        label1= ctk.CTkLabel(window, text=f" Error: {str(e)}", fg_color="black", text_color="red")
        label1.pack()

def on_click():
    label1 = ctk.CTkLabel(window, text="Locking workstation", text_color="blue", fg_color="black")
    label1.pack()
    window.after(1000, real_lock)

def on_click2():
    shutdown_confirmation_window()

def on_click3():
    label1 = ctk.CTkLabel(window, text="Closing script", text_color="blue", fg_color="black")
    label1.pack()
    window.after(1000, real_close)

button = ctk.CTkButton(
    window,
    text="Lock",
    command=on_click
)

button2 = ctk.CTkButton(
    window,
    text="Shutdown",
    command=on_click2
)

button3 = ctk.CTkButton(
    window,
    text="Close",
    fg_color="red",
    text_color="purple",
    hover_color="white",
    font=("Arial", 16, "bold"),
    command=on_click3
)

button4 = ctk.CTkButton(
    window,
    text="Test API",
    fg_color="purple",
    hover_color="green",
    font=("Arial", 16, "bold"),
    command=test_api_connection

)

button5 = ctk.CTkButton(
    window,
    text="Crash/Spam",
    fg_color="black",
    text_color="red",
    hover_color="white",
    font=("Arial", 16, "bold"),
    command=spam_and_crash_prep
)

button6 = ctk.CTkButton(
    window,
    text="Nuke Sequence",
    fg_color="red",
    hover_color="darkred",
    font=("Arial", 16, "bold", "italic"),
    command=nukesequenceprep
)


addip_frame = ctk.CTkFrame(window, fg_color="transparent")

button7 = ctk.CTkButton(
    addip_frame,
    text="Add IP whitelist",
    fg_color="darkgrey",
    font=("Arial", 16, "bold", "italic"),
    command=addipwhitelist
)

button8 = ctk.CTkButton(
    addip_frame,
    text="Add IP blacklist",
    fg_color="darkgrey",
    font=("Arial", 16, "bold", "italic"),
    command=addipblacklist
)


removeip_frame = ctk.CTkFrame(window, fg_color="transparent")


button9 = ctk.CTkButton(
    removeip_frame,
    text="Remove IP whitelist",
    fg_color="darkgrey",
    font=("Arial", 16, "bold", "italic"),
    command=removeipwhitelist
)

button10 = ctk.CTkButton(
    removeip_frame,
    text="Remove IP blacklist",
    fg_color="darkgrey",
    font=("Arial", 16, "bold", "italic"),
    command=removeipblacklist
)


button.pack()
button2.pack(pady=(20, 0))
button4.pack(pady=(20, 20))
if admin:
    button5.pack(pady=(0, 20))
    button6.pack(pady=(0, 20))
    button7.pack(side="left", padx=5)
    button8.pack(side="left", padx=5)
    button9.pack(side="left", padx=5)
    button10.pack(side="left", padx=5)
button3.pack()

addip_frame.pack(pady=(20, 20))
removeip_frame.pack(pady=(20, 20))

print(Fore.GREEN, """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡙⠛⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣜⣛⡛⢻⡖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡼⠛⠛⠛⠋⢻⡔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣾⣶⠶⠶⠿⠿⣶⢿⡳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡼⣢⣀⢀⣀⣀⢀⣠⡀⢻⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣼⠛⠉⠉⠉⠉⠁⠈⠉⠋⠛⢧⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠼⠥⠦⢡⡶⠶⠄⠖⠂⠶⣤⢞⣧⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣀⣠⣄⢀⣀⣀⣀⣄⢀⣤⡀⢀⡙⡛⢆⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢞⣟⣩⣭⠉⠈⠋⠉⠈⢉⠈⠉⠉⠚⠛⢣⣼⣆⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠟⢛⣭⣬⣤⡤⠴⠶⠢⠗⠟⠃⠾⠷⠆⣴⣤⡌⠙⣎⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢸⢿⣞⣟⣩⣥⣶⣶⣿⣾⣴⣖⣷⣤⣤⣤⡴⠄⠉⠰⠷⣿⡔⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣔⣿⣿⣽⣿⣿⣿⣿⡿⠿⠟⣟⣻⠿⠿⠞⢻⣛⣳⣚⣽⣧⣤⡼⡔⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣔⣿⣾⣿⣿⣯⣅⠉⠀⠤⠂⠀⢀⠀⠀⢀⠚⡉⠀⢁⡻⢗⢒⡚⣿⣯⡠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢔⣀⣿⢿⣚⣤⢽⣦⣀⡤⠤⠧⠖⠰⠒⡶⠷⣦⣴⡴⠋⠐⣀⣸⡍⢫⢿⣷⡢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⢺⣯⣭⣘⢛⡿⠾⣛⡍⠁⠂⠐⠐⠀⠐⠇⠦⠭⣽⣷⢦⣶⡛⠹⣧⣬⡾⠛⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⡞⣿⣧⣼⢛⠩⠴⠂⠁⠀⠀⠀⠀⡀⠐⠀⠀⠤⠄⡈⢙⡛⠯⣿⣯⣅⣬⡿⠿⣯⣧⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣛⣿⡿⢟⡅⢀⣆⣀⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣮⡻⠶⣏⡻⢿⣧⣽⠿⣿⣿⡇⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⡟⢋⣀⣦⣾⣿⠿⣿⣿⣿⡿⠉⢩⣽⢿⣿⣿⣿⡟⣿⣿⡿⢿⣷⣬⡻⣮⣁⣷⣴⢾⣛⣻⡄⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⠿⢋⣠⣬⣿⣿⣿⣿⡛⢿⣿⣿⣿⣀⡈⠁⣾⣻⣿⣿⢷⣿⣿⡟⠶⣟⢻⣷⣦⣙⣯⣿⣿⣟⣻⣾⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣿⢢⣾⣿⣿⣿⡏⡇⠸⡇⢸⣿⣿⢮⣿⣷⣿⣿⣿⠟⢃⣾⣿⣿⠣⣼⠋⣿⣿⣿⣿⣯⣿⣿⠟⣻⣶⣿⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣴⠷⢝⣆⠛⢿⢿⡧⡷⢻⡆⢳⡀⢻⣟⡿⣿⣛⣻⣚⣋⣠⡿⣿⣾⠇⡰⠋⢠⣯⣿⠿⢻⣽⣋⣿⣿⣟⣭⣙⣹⣏⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡴⣷⣦⢀⣘⠳⠓⠈⠤⠙⠳⠱⢀⠳⣀⠈⠛⠿⢿⢯⠽⠵⠾⠛⠋⢠⡔⠁⠤⠍⢋⣼⡷⣿⣵⢿⣿⢷⡚⠛⢿⣭⣹⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣽⣅⣀⠹⠿⡉⠁⠶⠶⠀⣀⠁⠀⠀⠀⣀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⡀⣩⣤⡴⣚⡿⠷⣟⡩⠟⠋⢀⣠⡽⢳⣾⣾⠟⠻⡁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣵⣈⠉⢿⣜⠋⠙⠓⠂⣄⡀⠈⠁⠐⠂⠠⡍⢈⡘⠒⠘⠒⢒⠓⢛⡃⢉⣡⠰⠒⠊⣁⣈⣥⠴⠂⠛⠛⢤⣄⣒⣠⣠⣩⣴⣷⠿⡅⠀⠀⠀⠀
⠀⠀⠀⢀⣙⣙⢿⣼⠛⠛⢷⣤⠆⢀⣀⠀⠙⠛⠰⠶⠤⠤⣤⣤⣤⣥⣤⣤⣤⠤⢤⡶⠷⠖⠛⠙⣉⣉⣤⣤⡦⠶⢖⠚⠋⠙⢧⣭⠁⠀⠙⡿⢻⠢⠀⠀⠀
⠀⠀⠠⣽⣿⡛⠛⠿⢶⣠⣤⡝⠃⡈⠉⠀⠓⠚⠷⠶⠴⢴⠤⠤⢴⣤⡤⠤⠤⡴⠤⠶⠖⠲⠚⠋⠉⢉⠁⢀⣀⣀⣾⣿⣦⣤⠴⠾⠿⠿⣿⡛⠛⢷⢀⠀⠀
⠀⠀⣽⡟⠻⣳⣴⡄⢤⣭⠷⠀⠙⠙⠐⠶⠆⢠⣄⠈⠉⠀⠶⠂⠠⠔⠀⠰⠴⠀⠺⠓⠂⠰⠾⠂⠚⢻⠇⠈⠉⠱⢄⢀⣀⣬⡙⢦⣦⣶⠿⡿⠷⣿⣧⢄⠀
⠐⠉⠛⠉⠛⠃⠈⠋⠀⠀⠉⠋⠁⠘⠋⠀⠚⠁⠀⠐⠛⠃⠀⠋⠁⠐⠂⠐⠂⠘⠁⠀⠋⠃⠐⠛⠓⠘⠛⠋⠘⠛⠋⠈⠉⠀⠀⠀⠙⠋⠉⠛⠛⠛⠛⠁⠂
""")
print(Style.RESET_ALL)
print(Fore.LIGHTMAGENTA_EX, "Booted Illuminati RCON")
print(Style.RESET_ALL)
if data.get("demo_mode") == True:
    print(Fore.LIGHTYELLOW_EX, f"Demo mode: True")
    print(Style.RESET_ALL)
if data.get("demo_mode") == False:
    print(Fore.LIGHTYELLOW_EX, f"Demo mode: False")
    print(Style.RESET_ALL)
print(Fore.CYAN, "Created by CrazyK")
print(Style.RESET_ALL)
print(Fore.LIGHTYELLOW_EX, f"Last Updated: {last_updated}")
print(f"Times ran {times_ran}")
print(Style.RESET_ALL)

#window.mainloop()
"""
All of the area below this was helped with generative AI.
I am slowly learning on how to work all of this, but,
I can assure you, everything above was human made by me.
"""
if __name__ == "__main__":
    import threading
    import uvicorn
    import socket

    # Get your real local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        WIFI_IP = s.getsockname()[0]
        s.close()
    except Exception:
        WIFI_IP = "127.0.0.1"

    def run_api():
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

    # Start API in background thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    print("------------------------------------------------------------")
    print("API is running")
    print(f"Local:   http://localhost:8000")
    print(f"Network: http://{WIFI_IP}:8000")
    print("------------------------------------------------------------")

    try:
        window.mainloop()
    finally:
        print("Closing...")
        print("Executing server shutdown")
        subprocess.run(["powershell", "-Command", "Get-Job | Stop-Job; Remove-Job *"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        subprocess.run(["taskkill", "/f", "/im", "python.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
