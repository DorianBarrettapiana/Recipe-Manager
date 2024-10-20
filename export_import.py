# Imports
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from utilities import *

# Export a recipe to a JSON file to share
def export_recipe(root):
    recipes = load_recipe()  
    if not recipes:
        return  

    export_window = tk.Toplevel()  
    export_window.iconbitmap(icon_path)  
    export_window.title("Export Recipes")
    export_window.geometry("480x380")
    export_window.resizable(False, False)

    export_window.transient(root)
    export_window.grab_set()

    canvas = tk.Canvas(export_window, width=480, height=380, relief="flat")
    canvas.pack(fill="both", expand=True)

    color1 = hex_to_rgb(black_gray)  
    color2 = hex_to_rgb(black_gray)

    canvas.update()
    create_gradient(canvas, color1, color2)
    
    frame = tk.Frame(canvas, relief="flat")
    frame.place(x=15, y=16, width=450, height=280)

    listbox = tk.Listbox(frame, width=53, height=20, **listbox_style)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Managing single, double click and ctrl click
    def on_single_click(event):
        index = listbox.nearest(event.y)  
        if index >= 0:
            if event.state & 0x0004: 
                if index in listbox.curselection():
                    listbox.selection_clear(index)
                else:
                    listbox.selection_set(index)
            else:
                listbox.selection_clear(0, tk.END) 
                listbox.selection_set(index)  

    def on_double_click(event):
        index = listbox.nearest(event.y) 
        if index >= 0:
            listbox.selection_clear(0, tk.END) 
            listbox.selection_set(index)  
            select_recipe()

    listbox.bind("<Button-1>", lambda event: root.after(0, on_single_click, event))
    listbox.bind("<Double-Button-1>", on_double_click)

    scrollbar = tk.Scrollbar(frame, relief="flat")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    for recipe_name in recipes.keys():
        listbox.insert(tk.END, recipe_name)

    def select_recipe():
        try:
            selected_indices = listbox.curselection()
            if not selected_indices:
                raise tk.TclError  

            selected_recipes = [listbox.get(i) for i in selected_indices]

            filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filepath:
                selected_data = {recipe_name: recipes[recipe_name] for recipe_name in selected_recipes}

                with open(filepath, 'w') as export_file:
                    json.dump(selected_data, export_file, indent=4)

                messagebox.showinfo("Exported", "Recipes successfully exported!")
        except tk.TclError:
            messagebox.showwarning("Select a Recipe", "Select one or more recipes to export.")

    select_button = tk.Button(canvas, text="Export", command=select_recipe, **button_style, height=1, width=15)
    select_button.bind("<Enter>", on_enter)
    select_button.bind("<Leave>", on_leave)
    select_button.place(x=150, y=322)

# Import an exported JSON file to add to the database
def import_recipe():
    filepath = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filepath:
        with open(filepath, 'r') as import_file:
            try:
                new_recipes = json.load(import_file)  
                recipes = load_recipe()  

                if isinstance(new_recipes, dict): 
                    added_recipes = []  
                    existing_recipes = []  

                    for recipe_name, recipe_data in new_recipes.items(): 
                        if recipe_name not in recipes:
                            recipes[recipe_name] = recipe_data  
                            added_recipes.append(recipe_name)  
                        else:
                            existing_recipes.append(recipe_name)  

                    with open(json_path, 'w') as f:
                        json.dump(recipes, f, indent=4)

                    if added_recipes:
                        messagebox.showinfo("Success", f"The following recipes have been imported:\n" + "\n".join(added_recipes))
                    if existing_recipes:
                        messagebox.showwarning("Clone !", f"The following recipes already exist and were not imported:\n" + "\n".join(existing_recipes))
                else:
                    messagebox.showerror("Error", "The file format is not valid. Expected a dictionary of recipes.")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Corrupted file.")