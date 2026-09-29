import tkinter as tk
import os
import random
import sys
from version import VERSION, REPO
import json
import threading
import urllib.request
import subprocess
import tempfile
from tkinter import messagebox

window = tk.Tk()
window.title("ClickCount")
window.geometry("300x200")


def resource_path(name):
    # exe: files are unpacked to a temp folder -> sys._MEIPASS
    # python: use the folder this .py file is in
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base, name)

window.iconbitmap(resource_path("mkwa.ico"))

with open(resource_path("quotes.txt"), encoding="utf-8") as f:
    quotes = [line for line in f.read().splitlines() if line.strip()]

DATA_DIR = os.path.join(os.environ["LOCALAPPDATA"], "ClickCounter")
COUNT_FILE = os.path.join(DATA_DIR, "count.txt")

def load_count():
    try:
        with open(COUNT_FILE, encoding="utf-8") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0

counter = load_count()

def save_count():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(COUNT_FILE, "w", encoding="utf-8") as f:
        f.write(str(counter))


def parse_version(v):
    return tuple(int(x) for x in v.lstrip("v").split("."))

def check_for_update():                      # runs in the background
    if not getattr(sys, "frozen", False):
        return                               # running from source: no auto-update
    try:
        url = f"https://api.github.com/repos/{REPO}/releases/latest"
        with urllib.request.urlopen(url, timeout=5) as r:
            release = json.load(r)
        latest = release["tag_name"]
        if parse_version(latest) > parse_version(VERSION):
            setup_url = next((a["browser_download_url"] for a in release["assets"]
                              if a["name"].endswith("-Setup.exe")), None)
            if setup_url:
                window.after(0, ask_update, latest, setup_url)
    except Exception:
        pass                                 # offline / no release: stay quiet


def ask_update(latest, setup_url):           # runs in the UI thread
    if messagebox.askyesno("Update available",
                           f"ClickCount {latest} is available (you have {VERSION}).\n\nUpdate now?"):
        window.title("ClickCount - downloading update...")
        threading.Thread(target=download_update, args=(setup_url,), daemon=True).start()

#
def download_update(setup_url):              # runs in the background
    def progress(blocks, block_size, total):
        if total > 0:
            pct = min(100, blocks * block_size * 100 // total)
            window.after(0, window.title, f"ClickCount - downloading update... {pct}%")
    try:
        path = os.path.join(tempfile.gettempdir(), "ClickCount-Setup.exe")
        urllib.request.urlretrieve(setup_url, path, progress)
        window.after(0, run_installer, path)
    except Exception as e:
        msg = f"Could not download the update:\n{e}"
        window.after(0, messagebox.showerror, "Update failed", msg)


def run_installer(path):                     # runs in the UI thread
    log = os.path.join(tempfile.gettempdir(), "ClickCount-update.log")
    env = dict(os.environ, PYINSTALLER_RESET_ENVIRONMENT="1")
    try:
        subprocess.Popen([path, "/SILENT", "/SUPPRESSMSGBOXES", "/NORESTART",
                          "/CLOSEAPPLICATIONS", "/FORCECLOSEAPPLICATIONS", f"/LOG={log}"], env=env)
    except OSError as e:
        messagebox.showerror("Update failed", f"Could not start the installer:\n{e}")
        window.title(f"ClickCount {VERSION}")
        return
    os._exit(0)                              # q

VERSION_FILE = os.path.join(DATA_DIR, "last_version.txt")

def check_just_updated():
    if not getattr(sys, "frozen", False):
        return                                   # running from source: skip
    try:
        with open(VERSION_FILE, encoding="utf-8") as f:
            previous = f.read().strip()
    except OSError:
        previous = None                          # first run after a fresh install
    if previous and previous != VERSION:
        messagebox.showinfo("Updated", f"ClickCount was updated from {previous} to {VERSION}.")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(VERSION)

def startup_checks():
    check_just_updated()          # waits here while the "Updated" message is open
    threading.Thread(target=check_for_update, daemon=True).start()

def update_label():
    label.config(text="count: "+ str(counter))

def clicked():
    global counter
    counter += 1
    update_label()
    save_count()  
    if counter % 10 == 0:
            quote_label.config(text=random.choice(quotes))

def reclicked():
    global counter
    counter = 0 

    update_label()
    save_count()  

label = tk.Label(window, font=("Arial", 12))

label.pack()
update_label()

button = tk.Button(window, text="click me", command=clicked)
button.pack()

resbutton = tk.Button(window, text="Reset", command=reclicked)
resbutton.pack()

quote_label = tk.Label(window, wraplength=280, font=("Arial", 10, "italic"))
quote_label.pack()


window.after(1000, lambda: threading.Thread(target=check_for_update, daemon=True).start())
##

window.after(500, startup_checks)
window.mainloop()