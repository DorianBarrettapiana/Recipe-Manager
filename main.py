# Imports
import tkinter as tk
from utilities import *
from add_recipe import *
from browse_recipe import *
from export_import import *

# Main window
def create_main_window():
    root = tk.Tk()
    root.title("Recipe Manager")
    root.geometry("700x380")
    root.iconbitmap(icon_path) 
    root.resizable(False, False)  

    # Create a canvas for the gradient background
    canvas = tk.Canvas(root, width=700, height=380)
    canvas.pack(fill="both", expand=True)

    # Colors for the gradient
    color1 = hex_to_rgb(beige)  # beige
    color2 = hex_to_rgb(pale_blue)  # pale blue

    root.update()  # Update the window to get canvas dimensions
    create_gradient(canvas, color2, color1)

    # Draw text directly on the canvas (no background)
    canvas.create_text(350, 75, text="Recipe Manager", font=("Calibri", 26, "bold"), fill=black_gray)

    # Create modern buttons
    button_style = {"font": ("Calibri", 14, "bold"), "height": 1, "width": 15, "borderwidth": 0, "background": pale_blue, "fg": dark_gray}

    add_button = tk.Button(root, text="Add a recipe", **button_style, activebackground=pale_blue, command=add_recipe)
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)
    canvas.create_window(350, 160, window=add_button)

    view_button = tk.Button(root, text="Browse recipes", **button_style, activebackground=pale_blue, command=view_recipe)
    view_button.bind("<Enter>", on_enter)
    view_button.bind("<Leave>", on_leave)
    canvas.create_window(350, 205, window=view_button)

    export_button = tk.Button(root, text="Export recipes", **button_style, activebackground=pale_blue, command=export_recipe)
    export_button.bind("<Enter>", on_enter)
    export_button.bind("<Leave>", on_leave)
    canvas.create_window(350, 250, window=export_button)

    import_button = tk.Button(root, text="Import recipes", **button_style, activebackground=pale_blue, command=import_recipe)
    import_button.bind("<Enter>", on_enter)
    import_button.bind("<Leave>", on_leave)
    canvas.create_window(350, 295, window=import_button)

    root.mainloop()

# Entry point
create_main_window()