# Imports
import json
import tkinter as tk
from tkinter import messagebox, filedialog
from utilities import *

# Export a recipe to a JSON file to share
def export_recipe():
    recipes = load_recipe()  
    if not recipes:
        return  

    export_window = tk.Toplevel()  
    export_window.iconbitmap(icon_path)  
    export_window.title("Export a recipe")
    export_window.geometry("480x500")
    export_window.resizable(False, False)  

    listbox = tk.Listbox(export_window, width=75, height=25, selectmode=tk.MULTIPLE)
    listbox.pack(pady=10)

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
                    json.dump(selected_data, export_file)

                messagebox.showinfo("Exported", "Recipes successfully exported!")
        except tk.TclError:
            messagebox.showwarning("Select a recipe", "Select one or more recipes to export.")

    select_button = tk.Button(export_window, text="Export", font=("Calibri", 12, "bold"), command=select_recipe, width=25)
    select_button.pack(pady=10)

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