import json, os, subprocess, sys, tkinter as tk
from tkinter import messagebox, simpledialog


HERE = os.path.dirname(os.path.abspath(sys.argv[0]))
CONFIG_FILE = os.path.join(HERE, "presets.json")

def load_presets():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Preset file not found at {CONFIG_FILE}")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f) 

def launch(cmd: str):
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

def add_preset():
    name = simpledialog.askstring("Add Preset", "Enter a name for the preset:")
    if not name:
        return
    
    # list of commands, edit JSON, quick add
    if name in presets:
        messagebox.showwarning("Preset already exists", "Please choose a different name")
        return
    
    commands = simpledialog.askstring("Add Preset", "Enter the commands for the preset (separated by commas):")
    if not commands:
        return
    
    # Turn the comma-separated string into a Python list
    cmd_list = [cmd.strip() for cmd in commands.split(",") if cmd.strip()]

    # Add new preset
    presets[name] = cmd_list

    # Save JSON file
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=2)

    # Refresh GUI
    refresh(listbox, presets)
    messagebox.showinfo("Success", f"Preset '{name}' added!")
    


def delete_preset(presets: dict, listbox: tk.Listbox):
    sel = listbox.curselection()
    if not sel:
        messagebox.showinfo("Pick a preset", "Select a preset to delete.")
        return
    name = listbox.get(sel[0])
    if messagebox.askyesno("Delete", f"Delete preset '{name}'?"):
        presets.pop(name, None)
        save_presets(presets)
        refresh(listbox, presets)

def refresh(listbox: tk.Listbox, presets: dict):
    listbox.delete(0, tk.END)
    for k in sorted(presets.keys()):
        listbox.insert(tk.END, k)

 

def main():
    try: 
        presets = load_presets()
    except Exception as e:
        messagebox.showerror("Error loading presets", str(e))
        return
    
    root = tk.Tk()
    root.title("Preset Launcher")
    root.geometry("420x480")
    root.resizable(False, False)
    
    tk.Label(root, text="Select a preset and click Run").pack(pady=8)

    lb = tk.Listbox(root, height=14)
    lb.pack(fill=tk.BOTH, expand=False, padx=12)

    refresh(lb, presets)

    btns = tk.Frame(root)
    btns.pack(fill=tk.X, padx=12, pady=10)

    def do_run():
        sel = lb.curselection()
        if not sel:
            messagebox.showinfo("No selection", "Pick a preset.")
            return
        name = lb.get(sel[0])
        run_preset(name, presets.get(name, []))
    
    def do_reload():
        nonlocal presets
        try:
            presets = load_presets()
            refresh(lb, presets)
            messagebox.showinfo("Reloaded", "Presets reloaded from file.")
        except Exception as e:
            messagebox.showerror("Reload failed", str(e))
    
    tk.Button(btns, text="Run", width=12, command=do_run).pack(side=tk.LEFT, padx=4)
    tk.Button(btns, text="Open Config", width=12, command=open_config).pack(side=tk.LEFT, padx=4)
    tk.Button(btns, text="Reload", width=12, command=do_reload).pack(side=tk.LEFT, padx=4)
    tk.Button(btns, text="+ New Preset", width=12, command=lambda: add_preset()).pack(side=tk.LEFT, padx=4)

    # Optional quick-add and delete for convenience
    extra = tk.Frame(root)
    extra.pack(fill=tk.X, padx=12)
    tk.Button(extra, text="Delete Preset", command=lambda: delete_preset(presets, lb)).pack(side=tk.LEFT, padx=4, pady=4)

    # Shortcut for run
    root.bind("<Return>", lambda _: do_run())

    root.mainloop()

if __name__ == "__main__":
    main()


if len(sys.argv) >= 3 and sys.argv[1] == "--run":
    preset_name = sys.argv[2]
    try:
        presets = load_presets()
        if preset_name in presets:
            run_preset(preset_name, presets[preset_name])
        else:
            messagebox.showerror("Preset not found", f"'{preset_name}' not in presets.json")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    sys.exit(0)
