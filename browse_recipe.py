# Imports
import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import base64
import os
from utilities import *

# Browse the data base and display recipes
def view_recipe(root):
    view_window = Toplevel()
    view_window.iconbitmap(icon_path)
    view_window.title("Recipes Displayer")
    view_window.geometry("480x420")
    view_window.resizable(False, False)

    view_window.transient(root)
    view_window.grab_set()

    canvas = tk.Canvas(view_window, width=480, height=420, relief="flat")
    canvas.pack(fill="both", expand=True)

    color1 = hex_to_rgb(black_gray)
    color2 = hex_to_rgb(black_gray)

    canvas.update()
    create_gradient(canvas, color1, color2)

    recipes = load_recipe()

    frame = tk.Frame(canvas, relief="flat")
    frame.place(x=15, y=16, width=450, height=280)

    recipe_listbox = tk.Listbox(frame, width=54, height=10, **listbox_style)
    recipe_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    def on_single_click(event):
            index = recipe_listbox.nearest(event.y)  
            if index >= 0:
                if event.state & 0x0004: 
                    if index in recipe_listbox.curselection():
                        recipe_listbox.selection_clear(index)
                    else:
                        recipe_listbox.selection_set(index)
                else:
                    recipe_listbox.selection_clear(0, tk.END) 
                    recipe_listbox.selection_set(index)  

    def on_double_click(event):
        index = recipe_listbox.nearest(event.y) 
        if index >= 0:
            recipe_listbox.selection_clear(0, tk.END) 
            recipe_listbox.selection_set(index)  
            show_selected_recipe()

    recipe_listbox.bind("<Button-1>", lambda event: root.after(0, on_single_click, event))
    recipe_listbox.bind("<Double-Button-1>", on_double_click)

    scrollbar = tk.Scrollbar(frame, relief="flat")
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
            #messagebox.showwarning("Warning", "Please select at least one recipe to delete.")
            return

        for index in reversed(selected_indices):  
            recipe_name = recipe_listbox.get(index).split(" - ")[0]  
            if recipe_name in recipes:
                del recipes[recipe_name]
                update_recipe_list() 

        save_recipes(recipes)
        # messagebox.showinfo("Success", "Selected recipes have been deleted.")

    delete_button = tk.Button(canvas, text="Delete Selected Recipes", command=delete_selected_recipes, **button_style)
    delete_button.bind("<Enter>", on_enter)
    delete_button.bind("<Leave>", on_leave)
    canvas.create_window(240, 385, window=delete_button)

    def show_selected_recipe():
        selected_index = recipe_listbox.curselection()
        if selected_index:  
            selected_recipe_name = recipe_listbox.get(selected_index[0]).split(" - ")[0]  
            selected_recipe = recipes[selected_recipe_name]

            recipe_detail_window = Toplevel(view_window)
            recipe_detail_window.iconbitmap(icon_path)
            recipe_detail_window.title(selected_recipe_name)
            recipe_detail_window.geometry("800x800")
            recipe_detail_window.resizable(False, False)

            canvas = tk.Canvas(recipe_detail_window, width=800, height=800, relief="flat")
            canvas.pack(fill="both", expand=True)

            color1 = hex_to_rgb(black_gray)
            color2 = hex_to_rgb(black_gray)

            canvas.update()
            create_gradient(canvas, color1, color2)

            canvas.create_text(400, 25, text="Number of People", font=("Calibri", 12, "bold"), fill=beige)
            
            num_people_entry = tk.Entry(canvas, width=6, justify="center", bg=beige, relief="flat")
            num_people_entry.insert(0, "1") 
            canvas.create_window(400, 50, window=num_people_entry)

            def validate_input(char):
                return char.isdigit()

            validate_command = recipe_detail_window.register(validate_input)  
            num_people_entry.config(validate="key", validatecommand=(validate_command, '%S'))

            recipe_canvas = tk.Canvas(recipe_detail_window, bg=beige, relief="flat")
            recipe_canvas.place(x=15, y=75, width=755, height=400)  

            v_scrollbar = tk.Scrollbar(recipe_detail_window, orient="vertical", command=recipe_canvas.yview, relief="flat")
            v_scrollbar.place(x=770, y=75, height=400)  

            recipe_canvas.configure(yscrollcommand=v_scrollbar.set)

            recipe_info_frame = tk.Frame(recipe_canvas, bg=beige, relief="flat")
            recipe_canvas.create_window((0, 0), window=recipe_info_frame, anchor="nw")

            def on_frame_configure(event):
                recipe_canvas.configure(scrollregion=recipe_canvas.bbox("all"))

            recipe_info_frame.bind("<Configure>", on_frame_configure)

            recipe_text = tk.Text(recipe_info_frame, width=755, height=400, padx=10, pady=10, bg=beige, fg=black_gray, font=("Calibri", 12), wrap="word", relief="flat")
            recipe_text.pack(fill="both", expand=True, anchor="nw") 
            v_scrollbar.config(command=recipe_text.yview)
            recipe_text.config(yscrollcommand=v_scrollbar.set)

            def display_recipe_details(num_people):
                ingredients_text = "\n".join(
                    f"{ingredient.split(':')[0]}: {float(ingredient.split(':')[1].split()[0]) * num_people} {ingredient.split(':')[1].split()[1]}"
                    for ingredient in selected_recipe['ingredients']
                )
                steps_text = "\n".join(selected_recipe['steps'])

                recipe_text.delete(1.0, tk.END)
                recipe_text.insert(tk.END, f"{selected_recipe['name']}\nDifficulty: {selected_recipe['difficulty']}\nPrice: {selected_recipe['price']}\n\nIngredients:\n{ingredients_text}\n\nSteps:\n{steps_text}")

            display_recipe_details(1)

            def update_recipe_details():
                try:
                    num_people = int(num_people_entry.get())
                    display_recipe_details(num_people) 
                except ValueError:
                    messagebox.showwarning("Error", "Enter a valid number.")

            update_button = tk.Button(canvas, text="Update", **button_style_mini, command=update_recipe_details)
            update_button.bind("<Enter>", on_enter)
            update_button.bind("<Leave>", on_leave)
            canvas.create_window(466, 50, window=update_button)

            if selected_recipe.get("image"):
                img_data = base64.b64decode(selected_recipe["image"])

                if not os.path.exists(im_dir):
                    os.makedirs(im_dir)

                with open(im_path, "wb") as img_file:
                    img_file.write(img_data)

                img_label = tk.Label(canvas, bg=beige, relief="flat")
                img_label.pack(side="bottom", pady=(20, 20))  

                img = Image.open(im_path)
                img_width, img_height = img.size
                img_ratio = img_width / img_height

                if img_ratio > 1:  
                    img = img.resize((int(282 * img_ratio), 282))  
                else:  
                    img = img.resize((int(282 * img_ratio), 282))  

                img_tk = ImageTk.PhotoImage(img)

                img_label.config(image=img_tk)
                img_label.image = img_tk  
            else:
                canvas.create_text(400, 642, text="No image found", font=("Calibri", 26, "bold"), fill=beige)

            clean_temp_files()  
        else:
            messagebox.showwarning("Error", "Please select a recipe.")

    recipe_listbox.bind('<Double-Button-1>', lambda event:show_selected_recipe())

    def sort_recipes(by, reverse=False, alphabetical=False):
        if alphabetical:
            sorted_recipes = sorted(recipes.items(), key=lambda x: x[0], reverse=reverse)
        else:
            sorted_recipes = sorted(recipes.items(), key=lambda x: x[1][by], reverse=reverse)

        recipe_listbox.delete(0, tk.END)
        for name, details in sorted_recipes:
            recipe_listbox.insert(tk.END, f"{name} - Difficulty: {details['difficulty']} - Price: {details['price']}")

    # Sorting buttons
    difficulty_asc_button = tk.Button(canvas, text="Difficulty ↑", command=lambda: sort_recipes('difficulty'), **button_style_mini)
    difficulty_asc_button.bind("<Enter>", on_enter)
    difficulty_asc_button.bind("<Leave>", on_leave)
    canvas.create_window(150, 316, window=difficulty_asc_button)

    difficulty_desc_button = tk.Button(canvas, text="Difficulty ↓", command=lambda: sort_recipes('difficulty', reverse=True), **button_style_mini)
    difficulty_desc_button.bind("<Enter>", on_enter)
    difficulty_desc_button.bind("<Leave>", on_leave)
    canvas.create_window(150, 345, window=difficulty_desc_button)

    price_asc_button = tk.Button(canvas, text="$ ↑", command=lambda: sort_recipes('price'), **button_style_mini)
    price_asc_button.bind("<Enter>", on_enter)
    price_asc_button.bind("<Leave>", on_leave)
    canvas.create_window(240, 316, window=price_asc_button)

    price_desc_button = tk.Button(canvas, text="$ ↓", command=lambda: sort_recipes('price', reverse=True), **button_style_mini)
    price_desc_button.bind("<Enter>", on_enter)
    price_desc_button.bind("<Leave>", on_leave)
    canvas.create_window(240, 345, window=price_desc_button)

    name_asc_button = tk.Button(canvas, text="A-Z", command=lambda: sort_recipes(by='name', alphabetical=True), **button_style_mini)
    name_asc_button.bind("<Enter>", on_enter)
    name_asc_button.bind("<Leave>", on_leave)
    canvas.create_window(330, 316, window=name_asc_button)

    name_desc_button = tk.Button(canvas, text="Z-A", command=lambda: sort_recipes(by='name', alphabetical=True, reverse=True), **button_style_mini)
    name_desc_button.bind("<Enter>", on_enter)
    name_desc_button.bind("<Leave>", on_leave)
    canvas.create_window(330, 345, window=name_desc_button)