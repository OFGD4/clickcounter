import tkinter as tk
import os
import random
import sys
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
window.mainloop()