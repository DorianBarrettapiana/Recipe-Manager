import json
import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel
import base64
import os

def load_recipe():
    if os.path.exists('recipes.json'):
        with open('recipes.json', 'r') as f:
            try:
                recipes = json.load(f)
                if isinstance(recipes, dict):
                    return recipes
                else:
                    messagebox.showerror("Error", "No dictionnary contained.")
                    return {}
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Corrupted file.")
                return {}
    else:
        messagebox.showerror("Error", "File doesn't exists.")
        return {}

def export_recipe():
    recipes = load_recipe()
    if not recipes:
        return  

    export_window = tk.Toplevel()
    export_window.title("Export a recipe")

    listbox = tk.Listbox(export_window, width=50, height=10)
    listbox.pack(pady=10)

    for recipe_name in recipes.keys():
        listbox.insert(tk.END, recipe_name)

    def select_recipe():
        try:
            selected = listbox.get(listbox.curselection())
            recipe = recipes[selected]  

            filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if filepath:
                with open(filepath, 'w') as export_file:
                    json.dump({selected: recipe}, export_file)  
                messagebox.showinfo("Exported", "Recipe successfully exported !")
        except tk.TclError:
            messagebox.showwarning("Select a recipe", "Select a recipe to export.")

    select_button = tk.Button(export_window, text="Export", command=select_recipe)
    select_button.pack(pady=10)

def import_recipe():
    filepath = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filepath:
        with open(filepath, 'r') as import_file:
            try:
                new_recipe = json.load(import_file)  
                recipes = load_recipe()  

                if isinstance(new_recipe, dict) and len(new_recipe) == 1:
                    recipe_name = list(new_recipe.keys())[0]
                    
                    if recipe_name not in recipes:
                        recipes[recipe_name] = new_recipe[recipe_name]
                        
                        with open('recipes.json', 'w') as f:
                            json.dump(recipes, f, indent=4)
                        messagebox.showinfo("Success", f"The recipe : '{recipe_name}' have been successfully exported.")
                    else:
                        messagebox.showwarning("Clone !", f"The recipe : '{recipe_name}' already exists.")
                else:
                    messagebox.showerror("Error", "The file is not valid.")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Corrupted file.")

def save_recipes(recipes, file_path='recipes.json'):
    """Sauvegarde les recipes dans un fichier JSON."""
    with open(file_path, 'w') as f:
        json.dump(recipes, f, indent=4)

def add_recipe():
    recipe_window = tk.Toplevel()
    recipe_window.title("Add a recipe")
    recipe_window.configure(bg='#F7F7F7') 
    recipe_window.geometry("800x600") 
    recipe_window.resizable(False, False)

    name_label = tk.Label(recipe_window, text="Recipe's Name", font=("Calibri", 18, "bold"), bg='#F7F7F7', fg='black')
    name_entry = tk.Entry(recipe_window, width=75)
    name_label.pack(pady=(25, 10))
    name_entry.pack(pady=(0, 20))

    difficulty_price_frame = tk.Frame(recipe_window, bg='#F7F7F7')
    difficulty_price_frame.pack(pady=(5, 20))

    difficulty_label = tk.Label(difficulty_price_frame, text="Difficulty", font=("Calibri", 12, "bold"), bg='#F7F7F7', fg='black')
    difficulty_var = tk.IntVar(value=1)
    difficulty_scale = tk.Scale(difficulty_price_frame, from_=1, to=5, orient=tk.HORIZONTAL, variable=difficulty_var)
    difficulty_label.pack(side=tk.LEFT, padx=(0, 25))
    difficulty_scale.pack(side=tk.LEFT, padx=(0, 20))

    price_label = tk.Label(difficulty_price_frame, text="Price", font=("Calibri", 12, "bold"), bg='#F7F7F7', fg='black')
    price_var = tk.IntVar(value=1)
    price_scale = tk.Scale(difficulty_price_frame, from_=1, to=5, orient=tk.HORIZONTAL, variable=price_var)
    price_label.pack(side=tk.LEFT, padx=(0, 25))
    price_scale.pack(side=tk.LEFT, padx=(0, 20))

    def upload_image():
        file_path = filedialog.askopenfilename(title="Select a photo", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                current_recipe["image"] = encoded_string
                image_label.config(text="Photo added : " + file_path.split("/")[-1])

    current_recipe = {}
    
    image_button = tk.Button(recipe_window, text="Add a photo", font=("Calibri", 12, "bold"), command=upload_image)
    image_button.pack(pady=(15, 15))
    image_label = tk.Label(recipe_window, text="", bg='#F7F7F7', fg='black')
    image_label.pack(pady=(0, 10))

    ingredients_steps_frame = tk.Frame(recipe_window, bg='#F7F7F7')
    ingredients_steps_frame.pack(pady=(2, 25))

    ingredient_label = tk.Label(ingredients_steps_frame, text="Ingredients", font=("Calibri", 15, "bold"), bg='#F7F7F7', fg='black')
    ingredient_label.grid(row=0, column=0, padx=(10, 10), pady=(0, 5), columnspan=3)  

    ingredient_listbox = tk.Listbox(ingredients_steps_frame, height=7, width=50)
    ingredient_listbox.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(0, 10)) 

    ingredient_entry = tk.Entry(ingredients_steps_frame, width=25)

    def validate_quantity(action, value_if_allowed):
        """Permet de n'accepter que des chiffres dans la quantité."""
        if action == '1':  
            return value_if_allowed.isdigit()
        return True

    vcmd = (recipe_window.register(validate_quantity), '%d', '%P')
    quantity_entry = tk.Entry(ingredients_steps_frame, width=8, validate='key', validatecommand=vcmd)
    unit_entry = tk.Entry(ingredients_steps_frame, width=8)

    ingredient_entry.grid(row=2, column=0, padx=(0, 2), pady=(0, 5))
    quantity_entry.grid(row=2, column=1, padx=(0, 2), pady=(0, 5))
    unit_entry.grid(row=2, column=2, padx=(0, 0), pady=(0, 5))

    def add_ingredient():
        ingredient = ingredient_entry.get().strip()
        quantity = quantity_entry.get().strip()
        unit = unit_entry.get().strip()
        if ingredient and quantity and unit:
            ingredient_listbox.insert(tk.END, f"{ingredient} : {quantity} {unit}")
            ingredient_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            unit_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Please fill all the entries.")

    add_ingredient_button = tk.Button(ingredients_steps_frame, text="Add the ingredient", font=("Calibri", 12, "bold"), command=add_ingredient)
    add_ingredient_button.grid(row=3, column=0, pady=(5, 10), columnspan=3)  # Bouton occupe 3 colonnes

    step_label = tk.Label(ingredients_steps_frame, text="Steps", font=("Calibri", 15, "bold"), bg='#F7F7F7', fg='black')
    step_label.grid(row=0, column=4, padx=(10, 5), pady=(0, 5))

    step_listbox = tk.Listbox(ingredients_steps_frame, height=7, width=50)
    step_listbox.grid(row=1, column=4, padx=(10, 5), pady=(0, 10))

    step_entry = tk.Entry(ingredients_steps_frame, width=50)
    step_entry.grid(row=2, column=4, padx=(10, 5), pady=(0, 5))

    def add_step():
        step = step_entry.get().strip()
        if step:
            step_listbox.insert(tk.END, step)
            step_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Please add a description for the step.")

    add_step_button = tk.Button(ingredients_steps_frame, text="Add the step", font=("Calibri", 12, "bold"), command=add_step)
    add_step_button.grid(row=3, column=4, pady=(5, 10))

    def save_recipe():
        recipe_name = name_entry.get().strip()
        if recipe_name:
            recipe = {
                'name': recipe_name,
                'difficulty': difficulty_var.get(),
                'price': price_var.get(),
                'ingredients': list(ingredient_listbox.get(0, tk.END)),
                'steps': list(step_listbox.get(0, tk.END)),
                'image': current_recipe.get("image", "")  
            }
            recipes[recipe_name] = recipe 
            save_recipes(recipes)  
            messagebox.showinfo("Success", "Recipe sucessfully added !")
            recipe_window.destroy()  
        else:
            messagebox.showwarning("Error", "The recipe's name is mandatory.")

    save_button = tk.Button(recipe_window, text="Save the recipe", font=("Calibri", 14, "bold"), command=save_recipe)
    save_button.pack(pady=(15, 15))

def view_recipe():
    view_window = Toplevel()
    view_window.title("Recipes Displayer")
    view_window.geometry("400x400")
    view_window.configure(bg='#F7F7F7')

    recipes = load_recipe()

    recipe_list_frame = tk.Frame(view_window, bg='#F7F7F7')
    recipe_list_frame.pack(pady=(10, 10))

    recipe_listbox = tk.Listbox(recipe_list_frame, width=80, height=15)
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

    def show_selected_recipe():
        selected_index = recipe_listbox.curselection()
        if selected_index:
            selected_recipe_name = recipe_listbox.get(selected_index).split(" - ")[0]  
            selected_recipe = recipes[selected_recipe_name]

            recipe_detail_window = Toplevel(view_window)
            recipe_detail_window.title(selected_recipe_name)
            recipe_detail_window.geometry("400x400")
            recipe_detail_window.configure(bg='#F7F7F7')

            tk.Label(recipe_detail_window, text="Number of people :", bg='#F7F7F7').pack(pady=(10, 0))
            num_people_entry = tk.Entry(recipe_detail_window)
            num_people_entry.pack(pady=(0, 10))

            def validate_input(char):
                return char.isdigit()  

            validate_command = recipe_detail_window.register(validate_input)
            num_people_entry.config(validate="key", validatecommand=(validate_command, '%S'))

            recipe_info_frame = tk.Frame(recipe_detail_window, bg='#F7F7F7')
            recipe_info_frame.pack(pady=(10, 10))

            def display_recipe_details():
                try:
                    num_people = int(num_people_entry.get())
        
                    ingredients_text = "\n".join(
                        f"{ingredient.split(':')[0]}: {float(ingredient.split(':')[1].split()[0]) * num_people} {ingredient.split(':')[1].split()[1]}"
                        for ingredient in selected_recipe['ingredients']
                    )
        
                    steps_text = "\n".join(selected_recipe['steps'])
        
                    recipe_label.config(text=f"Name: {selected_recipe['name']}\nDifficulty: {selected_recipe['difficulty']}\nPrix: {selected_recipe['price']}\n\nIngredients:\n{ingredients_text}\n\nÉtapes:\n{steps_text}")
                except ValueError:
                    messagebox.showwarning("Error", "Enter a valid number.")

            show_button = tk.Button(recipe_detail_window, text="Show", command=display_recipe_details)
            show_button.pack(pady=(10, 10))

            recipe_label = tk.Label(recipe_info_frame, bg='#F7F7F7', fg='black', font=("Calibri", 12))
            recipe_label.pack(pady=(10, 10))

            if selected_recipe.get("image"):
                img_data = base64.b64decode(selected_recipe["image"])
                with open("temp_image.png", "wb") as img_file:
                    img_file.write(img_data)

                img_label = tk.Label(recipe_detail_window, bg='#F7F7F7')
                img_label.pack(pady=(10, 10))

                img = tk.PhotoImage(file="temp_image.png")
                img_label.config(image=img)
                img_label.image = img  

            close_button = tk.Button(recipe_detail_window, text="Close", command=recipe_detail_window.destroy)
            close_button.pack(pady=(10, 10))
        else:
            messagebox.showwarning("Error", "Please select a recipe.")

    display_button = tk.Button(view_window, text="Display the selected recipe", command=show_selected_recipe)
    display_button.pack(pady=(10, 10))

    def sort_recipes(by):
        sorted_recipes = sorted(recipes.items(), key=lambda x: x[1][by])
        recipe_listbox.delete(0, tk.END)
        for name, details in sorted_recipes:
            recipe_listbox.insert(tk.END, f"{name} - Difficulty: {details['difficulty']} - Price: {details['price']}")

    sort_frame = tk.Frame(view_window, bg='#F7F7F7')
    sort_frame.pack(pady=(10, 10))

    difficulty_button = tk.Button(sort_frame, text="Sort by Difficulty", command=lambda: sort_recipes('difficulty'))
    difficulty_button.pack(side=tk.LEFT, padx=(10, 5))

    price_button = tk.Button(sort_frame, text="Sort by Price", command=lambda: sort_recipes('price'))
    price_button.pack(side=tk.LEFT, padx=(5, 10))

# Main window
def create_main_window():
    root = tk.Tk()
    root.title("Recipe Manager")
    root.configure(bg='#F7F7F7')
    root.geometry("800x400") 
    root.resizable(False, False)  

    label = tk.Label(root, text="Recipe Manager", font=("Calibri", 26, "bold"), bg='#F7F7F7', fg='black')
    label.pack(pady=(42, 42))

    add_button = tk.Button(root, text="Add a recipe", font=("Calibri", 14, "bold"), command=add_recipe)
    add_button.pack(pady=(10, 10))

    view_button = tk.Button(root, text="Browse recipes", font=("Calibri", 14, "bold"), command=view_recipe)
    view_button.pack(pady=(10, 10))

    export_button = tk.Button(root, text="Export a recipe",font=("Calibri", 12, "bold"), command=export_recipe)
    export_button.pack(pady=10)

    import_button = tk.Button(root, text="Import a recipe",font=("Calibri", 12, "bold"), command=import_recipe)
    import_button.pack(pady=10)

    root.mainloop()

recipes = load_recipe()
create_main_window()