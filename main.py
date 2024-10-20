import tkinter as tk
from utilities import *
from add_recipe import *
from browse_recipe import *
from export_import import *

def main():
    # Setting up the main frame
    root = tk.Tk()
    root.title("Recipe Manager")
    root.geometry("700x380")
    root.iconbitmap(icon_path) 
    root.resizable(False, False)  

    # Create a canvas for the background
    canvas = tk.Canvas(root, width=700, height=380)
    canvas.pack(fill="both", expand=True)

    # Colors for the gradient
    color1 = hex_to_rgb(black_gray)  
    color2 = hex_to_rgb(black_gray)  

    root.update()
    create_gradient(canvas, color1, color2)

    # Draw text directly on the canvas
    canvas.create_text(350, 75, text="Recipe Manager", font=("Calibri", 26, "bold"), fill=beige)

    # Adding all the bottom
    add_button = tk.Button(root, text="Add a recipe", height = 1, width = 15, **button_style, activebackground=pale_blue, command=lambda:add_recipe(root))
    add_button.bind("<Enter>", on_enter)
    add_button.bind("<Leave>", on_leave)
    canvas.create_window(350, 160, window=add_button)

    view_button = tk.Button(root, text="Browse recipes", height = 1, width = 15, **button_style, activebackground=pale_blue, command=lambda:view_recipe(root))
    view_button.bind("<Enter>", on_enter)
    view_button.bind("<Leave>", on_leave)
    canvas.create_window(350, 205, window=view_button)

    export_button = tk.Button(root, text="Export recipes", height = 1, width = 15, **button_style, activebackground=pale_blue, command=lambda:export_recipe(root))
    export_button.bind("<Enter>", on_enter)
    export_button.bind("<Leave>", on_leave)
    canvas.create_window(350, 250, window=export_button)

    import_button = tk.Button(root, text="Import recipes", height = 1, width = 15, **button_style, activebackground=pale_blue, command=import_recipe)
    import_button.bind("<Enter>", on_enter)
    import_button.bind("<Leave>", on_leave)
    canvas.create_window(350, 295, window=import_button)

    root.mainloop()

# Entry point
if __name__ == "__main__":
    main()