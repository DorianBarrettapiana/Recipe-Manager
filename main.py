import tkinter as tk
from PIL import Image, ImageTk
from utilities import *
from add_recipe import *
from browse_recipe import *
from export_import import *
from settings import *

def main():
    root = tk.Tk() # Initialize main window
    root.title("Recipe Manager") # Title of the window
    root.geometry("700x380") # Size
    root.configure(bg=black_gray) # Background color
    root.iconbitmap(icon_path) # Icon of the window
    root.resizable(False, False) # Non resizable 

    # Configuration of columns
    root.grid_columnconfigure(0, weight=1)  # Left
    root.grid_columnconfigure(2, weight=1)  # Center (buttons)
    root.grid_columnconfigure(4, weight=1)  # Right

    # Title
    title = tk.Label(root, text="Recipe Manager", **label_tit_style)
    title.grid(row=0, column=1, columnspan=3, pady=(33, 30), sticky="n")

    # Settings button
    settings_img = Image.open(settings_icon_path) # Usage of an image as button support
    settings_img = settings_img.resize((22, 22)) # Resizing it
    settings_im = ImageTk.PhotoImage(settings_img)
    settings_button = tk.Button(root, image=settings_im, command=lambda: settings(root), **button_im_style)
    settings_button.image = settings_im  # Reference to the image to keep it displayed and not collected by garbage collector
    settings_button.grid(row=0, column=4, sticky="ne", padx=(0, 33), pady=(33, 0))

    # Main buttons
    add_button = tk.Button(root, text="Add a recipe", command=lambda: add_recipe(root), **button_style)
    add_button.grid(row=1, column=2, pady=(11, 11))
    # ---------------------------------------------------------------------------------------------------------
    view_button = tk.Button(root, text="Browse recipes", command=lambda: view_recipe(root), **button_style)
    view_button.grid(row=2, column=2, pady=(11, 11))
    # ---------------------------------------------------------------------------------------------------------
    export_button = tk.Button(root, text="Export recipes", command=lambda: export(root), **button_style)
    export_button.grid(row=3, column=2, pady=(11, 11))
    # ---------------------------------------------------------------------------------------------------------
    import_button = tk.Button(root, text="Import recipes", command=import_recipe, **button_style)
    import_button.grid(row=4, column=2, pady=(11, 11))

    # Version of the app 
    version = tk.Label(root, text="v1.1", **label_mini_style)
    version.grid(row=6, column=0, padx=(33, 0), pady=(0, 33), sticky="w")

    root.mainloop()

# Entry point
if __name__ == "__main__":
    main()