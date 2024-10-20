import tkinter as tk
from tkinter import filedialog, messagebox
import base64
from utilities import *

# Add a recipe to the data base
def add_recipe(root):
    recipe_window = tk.Toplevel()
    recipe_window.iconbitmap(icon_path)
    recipe_window.title("Add a recipe")
    recipe_window.configure(bg=black_gray) 
    recipe_window.geometry("700x700") 
    recipe_window.resizable(False, False)

    name_label = tk.Label(recipe_window, text="Recipe's Name", font=("Calibri", 18, "bold"), bg=black_gray, fg=beige)
    name_entry = tk.Entry(recipe_window, width=50)
    name_label.pack(pady=(20, 10))
    name_entry.pack(pady=(0, 20))

    difficulty_price_frame = tk.Frame(recipe_window, bg=black_gray)
    difficulty_price_frame.pack(pady=(5, 20))

    difficulty_label = tk.Label(difficulty_price_frame, text="Difficulty", font=("Calibri", 12, "bold"), bg=black_gray, fg=beige)
    difficulty_var = tk.IntVar(value=1)
    difficulty_scale = tk.Scale(difficulty_price_frame, from_=1, to=5, orient=tk.HORIZONTAL, variable=difficulty_var, sliderrelief="flat", bg=black_gray, fg=beige)
    difficulty_label.pack(side=tk.LEFT, padx=(0, 50))
    difficulty_scale.pack(side=tk.LEFT, padx=(0, 50))

    price_label = tk.Label(difficulty_price_frame, text="Price", font=("Calibri", 12, "bold"), bg=black_gray, fg=beige)
    price_var = tk.IntVar(value=1)
    price_scale = tk.Scale(difficulty_price_frame, from_=1, to=5, orient=tk.HORIZONTAL, variable=price_var, sliderrelief="flat", bg=black_gray, fg=beige)
    price_label.pack(side=tk.LEFT, padx=(0, 50))
    price_scale.pack(side=tk.LEFT, padx=(0, 50))

    # Add an image to the JSON and encode it in base64
    def upload_image():
        file_path = filedialog.askopenfilename(title="Select a photo", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                current_recipe["image"] = encoded_string
                image_label.config(text="Photo added : " + file_path.split("/")[-1])

    current_recipe = {}
    
    image_button = tk.Button(recipe_window, text="Add a photo", font=("Calibri", 12, "bold"), command=upload_image, width=22, **button_style_2)
    image_button.bind("<Enter>", on_enter)
    image_button.bind("<Leave>", on_leave)
    image_button.pack(pady=(5, 5))
    image_label = tk.Label(recipe_window, text="", bg=black_gray, fg=beige)
    image_label.pack(pady=(0, 10))

    ingredients_steps_frame = tk.Frame(recipe_window, bg=black_gray)
    ingredients_steps_frame.pack(pady=(2, 25))

    ingredient_label = tk.Label(ingredients_steps_frame, text="Ingredients", font=("Calibri", 15, "bold"), bg=black_gray, fg=beige)
    info_label = tk.Label(ingredients_steps_frame, text="All quantities are for 1 person", font=("Calibri", 9, "bold"), bg=black_gray, fg=beige)
    ingredient_label.grid(row=0, column=0, padx=(3, 2), pady=(0, 0), columnspan=3)
    info_label.grid(row=1, column=0, padx=(3, 12), pady=(0, 0), columnspan=3)

    ingredient_listbox = tk.Listbox(ingredients_steps_frame, height=10, width=50, **listbox_style_2)
    ingredient_listbox.grid(row=2, column=0, columnspan=3, padx=(10, 10), pady=(0, 0)) 
    info_2_label = tk.Label(ingredients_steps_frame, text="         Ingredient                Quantity         Unit", font=("Calibri", 12), bg=black_gray, fg=beige)
    info_2_label.grid(row=3, column=0, padx=(3, 12), pady=(0, 5), columnspan=3)
    ingredient_entry = tk.Entry(ingredients_steps_frame, width=25)

    def validate_quantity(action, value_if_allowed):
        if action == '1':  
            return value_if_allowed.isdigit()
        return True

    vcmd = (recipe_window.register(validate_quantity), '%d', '%P')
    quantity_entry = tk.Entry(ingredients_steps_frame, width=8, validate='key', validatecommand=vcmd)
    unit_entry = tk.Entry(ingredients_steps_frame, width=8)

    ingredient_entry.grid(row=4, column=0, padx=(0, 2), pady=(0, 5))
    quantity_entry.grid(row=4, column=1, padx=(0, 2), pady=(0, 5))
    unit_entry.grid(row=4, column=2, padx=(0, 0), pady=(0, 5))

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

    def del_ingredient():
        ingredient = ingredient_listbox.curselection()
        if ingredient:
            ingredient_listbox.delete(0)
        #else:
            # messagebox.showwarning("Error", "You must select an ingredient.")

    add_ingredient_button = tk.Button(ingredients_steps_frame, text="Add the ingredient", font=("Calibri", 12, "bold"), command=add_ingredient, width=37, **button_style_2)
    add_ingredient_button.bind("<Enter>", on_enter)
    add_ingredient_button.bind("<Leave>", on_leave)
    add_ingredient_button.grid(row=5, column=0, pady=(5, 10), columnspan=3) 

    del_ingredient_button = tk.Button(ingredients_steps_frame, text="Delete the ingredient", font=("Calibri", 12, "bold"), command=del_ingredient, width=37, **button_style_2)
    del_ingredient_button.bind("<Enter>", on_enter)
    del_ingredient_button.bind("<Leave>", on_leave)
    del_ingredient_button.grid(row=6, column=0, pady=(0, 10), columnspan=3)

    step_label = tk.Label(ingredients_steps_frame, text="Steps", font=("Calibri", 15, "bold"), bg=black_gray, fg=beige)
    step_label.grid(row=0, column=4, padx=(10, 5), pady=(0, 5))

    step_listbox = tk.Listbox(ingredients_steps_frame, height=10, width=50, **listbox_style_2)
    step_listbox.grid(row=2, column=4, padx=(10, 5), pady=(0, 0))

    step_entry = tk.Entry(ingredients_steps_frame, width=50)
    step_entry.grid(row=4, column=4, padx=(10, 5), pady=(0, 5))

    def add_step():
        step = step_entry.get().strip()
        if step:
            step_listbox.insert(tk.END, step)
            step_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Please add a description for the step.")

    def del_step():
        selected = step_listbox.curselection()
        if selected:
            step_listbox.delete(0)
        #else:
            #messagebox.showwarning("Error", "You must select a step.")

    add_step_button = tk.Button(ingredients_steps_frame, text="Add the step", font=("Calibri", 12, "bold"), command=add_step, width=37, **button_style_2)
    add_step_button.bind("<Enter>", on_enter)
    add_step_button.bind("<Leave>", on_leave)
    add_step_button.grid(row=5, column=4, pady=(5, 10))

    del_step_button = tk.Button(ingredients_steps_frame, text="Delete the step", font=("Calibri", 12, "bold"), command=del_step, width=37, **button_style_2)
    del_step_button.bind("<Enter>", on_enter)
    del_step_button.bind("<Leave>", on_leave)
    del_step_button.grid(row=6, column=4, pady=(0, 10), columnspan=3)

    # Edit the ingredient when double click
    def edit_ingredient_popup(index):
        ingredient_data = ingredient_listbox.get(index)
        
        ingredient_parts = ingredient_data.split(':')
        name_part = ingredient_parts[0].strip()
        quantity_unit = ingredient_parts[1].strip().split()
        quantity_part = quantity_unit[0]
        unit_part = quantity_unit[1] if len(quantity_unit) > 1 else ''
        
        popup = tk.Toplevel()
        popup.iconbitmap(icon_path)
        popup.geometry("280x140")
        popup.configure(bg=beige)
        popup.resizable(False, False)
        popup.title("Edit Ingredient")
        
        tk.Label(popup, text="Ingredient", bg=beige, font = ("Calibri", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        ingredient_name_entry = tk.Entry(popup, width=25, bg=beige, font = ("Calibri", 10, "bold"))
        ingredient_name_entry.grid(row=0, column=1, padx=5, pady=5)
        ingredient_name_entry.insert(0, name_part)
        
        tk.Label(popup, text="Quantity", bg=beige, font = ("Calibri", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
        ingredient_quantity_entry = tk.Entry(popup, width=10, validate='key', validatecommand=vcmd, bg=beige, font = ("Calibri", 10, "bold"))
        ingredient_quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        ingredient_quantity_entry.insert(0, quantity_part)
        
        tk.Label(popup, text="Unit", bg=beige, font = ("Calibri", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
        ingredient_unit_entry = tk.Entry(popup, width=10, bg=beige, font = ("Calibri", 10, "bold"))
        ingredient_unit_entry.grid(row=2, column=1, padx=5, pady=5)
        ingredient_unit_entry.insert(0, unit_part)
        
        def save_ingredient():
            new_name = ingredient_name_entry.get().strip()
            new_quantity = ingredient_quantity_entry.get().strip()
            new_unit = ingredient_unit_entry.get().strip()
            
            if new_name and new_quantity and new_unit:
                ingredient_listbox.delete(index)
                ingredient_listbox.insert(index, f"{new_name} : {new_quantity} {new_unit}")
                popup.destroy()
            else:
                messagebox.showwarning("Error", "All fields must be filled.")
        
        save_button = tk.Button(popup, text="Save", command=save_ingredient, **button_style_mini)
        save_button.bind("<Enter>", on_enter)
        save_button.bind("<Leave>", on_leave)
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    # Edit the step when double click
    def edit_step_popup(index):
        step_data = step_listbox.get(index)
        
        popup = tk.Toplevel()
        popup.iconbitmap(icon_path)
        popup.geometry("360x75")
        popup.configure(bg=beige)
        popup.resizable(False, False)
        popup.title("Edit Step")
        
        tk.Label(popup, text="Step", bg=beige, font = ("Calibri", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        step_entry_popup = tk.Entry(popup, width=50, bg=beige, font = ("Calibri", 10, "bold"))
        step_entry_popup.grid(row=0, column=1, padx=5, pady=5)
        step_entry_popup.insert(0, step_data)
        
        def save_step():
            new_step = step_entry_popup.get().strip()
            if new_step:
                step_listbox.delete(index)
                step_listbox.insert(index, new_step)
                popup.destroy()
            else:
                messagebox.showwarning("Error", "Step cannot be empty.")
        
        save_button = tk.Button(popup, text="Save", command=save_step, **button_style_mini)
        save_button.bind("<Enter>", on_enter)
        save_button.bind("<Leave>", on_leave)
        save_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    ingredient_listbox.bind('<Double-Button-1>', lambda event: edit_ingredient_popup(ingredient_listbox.curselection()[0]))
    step_listbox.bind('<Double-Button-1>', lambda event: edit_step_popup(step_listbox.curselection()[0]))

    # Save the recipe with the right format in the JSON
    def save_recipe():
        recipes = load_recipe()
        recipe_name = name_entry.get().strip()
        ingredient_listbox_val = ingredient_listbox.get(0)
        step_listbox_val = step_listbox.get(0)
        if recipe_name and ingredient_listbox_val and step_listbox_val:
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
            messagebox.showwarning("Error", "Please fill all the entries.")

    save_button = tk.Button(recipe_window, text="Save the recipe", font=("Calibri", 14, "bold"), command=save_recipe, width=62, **button_style_2)
    save_button.bind("<Enter>", on_enter)
    save_button.bind("<Leave>", on_leave)
    save_button.pack(pady=(10, 10))