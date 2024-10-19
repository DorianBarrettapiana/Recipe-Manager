# Imports
import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import base64
import os
from utilities import *

# Browse the data base and display recipes
def view_recipe():
    view_window = Toplevel()
    view_window.iconbitmap(icon_path)
    view_window.title("Recipes Displayer")
    view_window.geometry("480x550")
    view_window.resizable(False, False)
    view_window.configure(bg=beige)

    recipes = load_recipe()

    recipe_list_frame = tk.Frame(view_window, bg=beige)
    recipe_list_frame.pack(pady=(10, 10))

    recipe_listbox = tk.Listbox(recipe_list_frame, width=75, height=25, selectmode=tk.MULTIPLE)
    recipe_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar = tk.Scrollbar(recipe_list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    recipe_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=recipe_listbox.yview)

    def update_recipe_list():
        recipe_listbox.delete(0, tk.END)  
        for name, details in recipes.items():
            recipe_listbox.insert(tk.END, f"{name} - Difficulty: {details['difficulty']} - Price: {details['price']}")

    update_recipe_list()

    def delete_selected_recipes():
        selected_indices = recipe_listbox.curselection() 
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one recipe to delete.")
            return

        #recipes = load_recipe()

        for index in reversed(selected_indices):  
            recipe_name = recipe_listbox.get(index).split(" - ")[0]  
            if recipe_name in recipes:
                del recipes[recipe_name]
                update_recipe_list() 
                #recipe_listbox.delete(index) 

        save_recipes(recipes)
        messagebox.showinfo("Success", "Selected recipes have been deleted.")

    delete_button = tk.Button(view_window, text="Delete Selected Recipes", command=delete_selected_recipes)
    delete_button.pack(pady=(10, 10))

    def show_selected_recipe(index):
        selected_index = recipe_listbox.curselection()
        if selected_index:  
            selected_recipe_name = recipe_listbox.get(selected_index[0]).split(" - ")[0]  
            selected_recipe = recipes[selected_recipe_name]

            recipe_detail_window = Toplevel(view_window)
            recipe_detail_window.iconbitmap(icon_path)
            recipe_detail_window.title(selected_recipe_name)
            recipe_detail_window.geometry("640x480")
            recipe_detail_window.configure(bg=beige)

            tk.Label(recipe_detail_window, text="Number of people:", bg=beige).pack(pady=(10, 0))
            
            num_people_entry = tk.Entry(recipe_detail_window)
            num_people_entry.insert(0, "1") 
            num_people_entry.pack(pady=(0, 10))

            def validate_input(char):
                return char.isdigit()  

            validate_command = recipe_detail_window.register(validate_input)
            num_people_entry.config(validate="key", validatecommand=(validate_command, '%S'))

            recipe_info_frame = tk.Frame(recipe_detail_window, bg=beige)
            recipe_info_frame.pack(pady=(10, 10))

            recipe_label = tk.Label(recipe_info_frame, bg=beige, fg='black', font=("Calibri", 12))
            recipe_label.pack(pady=(10, 10))

            def display_recipe_details(num_people):
                ingredients_text = "\n".join(
                    f"{ingredient.split(':')[0]}: {float(ingredient.split(':')[1].split()[0]) * num_people} {ingredient.split(':')[1].split()[1]}"
                    for ingredient in selected_recipe['ingredients']
                )
                steps_text = "\n".join(selected_recipe['steps'])

                recipe_label.config(text=f"Name: {selected_recipe['name']}\nDifficulty: {selected_recipe['difficulty']}\nPrix: {selected_recipe['price']}\n\nIngredients:\n{ingredients_text}\n\nÉtapes:\n{steps_text}")

            display_recipe_details(1)

            def update_recipe_details():
                try:
                    num_people = int(num_people_entry.get())
                    display_recipe_details(num_people) 
                except ValueError:
                    messagebox.showwarning("Error", "Enter a valid number.")

            update_button = tk.Button(recipe_detail_window, text="Update", command=update_recipe_details)
            update_button.pack(pady=(10, 10))

            if selected_recipe.get("image"):
                img_data = base64.b64decode(selected_recipe["image"])

                if not os.path.exists(im_dir):
                    os.makedirs(im_dir)

                with open(im_path, "wb") as img_file:
                    img_file.write(img_data)

                img_label = tk.Label(recipe_detail_window, bg=beige)
                img_label.pack(pady=(10, 10))

                img = Image.open(im_path)
                img_width, img_height = img.size
                img_ratio = img_width / img_height

                if img_ratio > 1:  
                    img = img.resize((300, int(300 / img_ratio))) 
                else:  
                    img = img.resize((int(500 * img_ratio), 500)) 

                img_tk = ImageTk.PhotoImage(img)

                img_label.config(image=img_tk)
                img_label.image = img_tk  

            close_button = tk.Button(recipe_detail_window, text="Close", command=recipe_detail_window.destroy)
            close_button.pack(pady=(10, 10))

            clean_temp_files()
        else:
            messagebox.showwarning("Error", "Please select a recipe.")

    recipe_listbox.bind('<Double-Button-1>', lambda event: show_selected_recipe(recipe_listbox.curselection()))

    def sort_recipes(by, reverse=False, alphabetical=False):
        if alphabetical:
            sorted_recipes = sorted(recipes.items(), key=lambda x: x[0], reverse=reverse)
        else:
            sorted_recipes = sorted(recipes.items(), key=lambda x: x[1][by], reverse=reverse)

        recipe_listbox.delete(0, tk.END)
        for name, details in sorted_recipes:
            recipe_listbox.insert(tk.END, f"{name} - Difficulty: {details['difficulty']} - Price: {details['price']}")

    sort_frame = tk.Frame(view_window, bg=beige)
    sort_frame.pack(pady=(10, 10))

    difficulty_asc_button = tk.Button(sort_frame, text="Sort by Difficulty ↑", command=lambda: sort_recipes('difficulty'))
    difficulty_asc_button.grid(row=0, column=0, padx=(10, 5))

    difficulty_desc_button = tk.Button(sort_frame, text="Sort by Difficulty ↓", command=lambda: sort_recipes('difficulty', reverse=True))
    difficulty_desc_button.grid(row=1, column=0, padx=(10, 5))

    price_asc_button = tk.Button(sort_frame, text="Sort by Price ↑", command=lambda: sort_recipes('price'))
    price_asc_button.grid(row=0, column=1, padx=(10, 5))

    price_desc_button = tk.Button(sort_frame, text="Sort by Price ↓", command=lambda: sort_recipes('price', reverse=True))
    price_desc_button.grid(row=1, column=1, padx=(10, 5))

    name_asc_button = tk.Button(sort_frame, text="Sort by Name A-Z", command=lambda: sort_recipes(by='name', alphabetical=True))
    name_asc_button.grid(row=0, column=2, padx=(10, 5))

    name_desc_button = tk.Button(sort_frame, text="Sort by Name Z-A", command=lambda: sort_recipes(by='name', alphabetical=True, reverse=True))
    name_desc_button.grid(row=1, column=2, padx=(10, 5))