# Imports
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from utilities import *

# Export a recipe to a JSON file to share
def export(root):
    # Only start if recipes exist
    recipes = load_recipe()  
    if not recipes:
        return  

    export_window = tk.Toplevel() 
    export_window.iconbitmap(icon_path)  
    export_window.title("Export Recipes")
    export_window.geometry("480x380")
    export_window.configure(bg=black_gray) 
    export_window.resizable(False, False)

    export_window.transient(root)
    export_window.grab_set()

    listbox = tk.Listbox(export_window, width=56, height=15, **listbox_style)
    listbox.grid(row=0, column=0, padx=(6, 0), pady=(5, 15), sticky='nw')

    scrollbar = tk.Scrollbar(export_window, relief="flat")
    scrollbar.grid(row=0, column=1, padx=(0, 0), pady=(5, 15), sticky='ns')  # Stick to 'ns' for vertical stretching
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    # Single, double click and ctrl click
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
            export_recipe()

    listbox.bind("<Button-1>", lambda event: root.after(0, on_single_click, event))
    listbox.bind("<Double-Button-1>", on_double_click)

    for recipe_name in recipes.keys():
        listbox.insert(tk.END, recipe_name)

    def export_recipe():
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

    select_button = tk.Button(export_window, text="Export", command=export_recipe, **button_style)
    select_button.grid(row=1, column=0, columnspan=2, pady=(0, 8))  # Center by spanning both columns

# Import an exported JSON file to add to the database
def import_recipe():
    filepath = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")]) # Search for JSON file in the computer files
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