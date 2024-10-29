import tkinter as tk
from utilities import *

def settings(root):
    settings_window = tk.Toplevel()
    settings_window.iconbitmap(icon_path)
    settings_window.title("Settings")
    settings_window.configure(bg=black_gray) 
    settings_window.geometry("220x220") 
    settings_window.resizable(False, False)

    settings_window.transient(root) # Take the lead over the main window
    settings_window.grab_set() # As long as actions are done on this window

    name_label = tk.Label(settings_window, text="Coming soon", **label_style)
    name_label.grid(padx=(60, 60), pady=(85, 85), sticky='n')