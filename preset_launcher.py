import json, os, subprocess, sys, tkinter as tk
from tkinter import messagebox, simpledialog


HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
CONFIG_FILE = os.path.join(HERE, "presets.json")

def load_presets():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Preset file not found at {CONFIG_FILE}")
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f) 

def launch(cmd: strD):
    """
    Try to open os.startfile for URLs (spotify:, steam://, etc)
    for commands with arguments (exe + flags / URLs)
    """

    try:
        os.startfile(cmd)
        return
    except Exception as e:
        print(f"Error launching {cmd}: {e}")
    
    try:
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        messagebox.showerror("Launch failed", f"{cmd}\n\n{e}")
    
    def run_preset(preset_name: str, commands: list[str]):
        """
        Run a preset by name, with a list of commands
        """
        failed = []
        for c in commands:
            try:
                launch(c)
            except Exception as e: 
                failed.append((c, str(e)))
            
        if failed:
            msg = "\n\n".join(f"{c}\n{err}" for c, err in failed)
            messagebox.showwarning("Some items failed to launch", msg)
    
    def open_config():
        try: 
            os.startfile(CONFIG_FILE)
        except Exception as e:
            messagebox.showerror("Error opening config", str(e))
    
    def save_presets(presets: dict):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2)
    
    
    

