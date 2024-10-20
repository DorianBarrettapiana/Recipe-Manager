import os
import sys
import json
import tkinter as tk
from tkinter import messagebox

# Definition of colors
beige = "#F7F7F7"         # Light beige
light_gray = "#D3D3D3"    # Light Gray
pale_blue = "#A3C1DA"     # Pale Blue
pale_pink = "#F8D7DA"     # Pale Pink
sage_green = "#B7C4A1"    # Sage Green
light_brown = "#A58A68"   # Light Brown
pastel_yellow = "#FFFACD" # Pastel Yellow
bluish_gray = "#BCCCDC"   # Bluish Gray
dark_gray = "#4A4A4A"     # Dark Gray
black_gray =  "#2C2C2C"   # Black Gray

# Styles
listbox_style = {"font": ("Calibri", 12), "background": beige, "fg": black_gray, "selectmode":tk.MULTIPLE,"selectbackground": sage_green, "selectforeground": black_gray, "borderwidth": 0, "relief": "flat"}
listbox_style_2 = {"background": beige, "fg": black_gray, "selectmode":tk.MULTIPLE,"selectbackground": sage_green, "selectforeground": black_gray, "borderwidth": 0, "relief": "flat"}
button_style = {"font": ("Calibri", 14, "bold"), "borderwidth": 0, "background": pale_blue, "fg": black_gray, "relief": "flat"}
button_style_mini = {"font": ("Calibri", 10, "bold"), "borderwidth": 0, "background": pale_blue, "fg": black_gray, "relief": "flat"}
button_style_2 = {"borderwidth": 0, "background": pale_blue, "fg": black_gray, "relief": "flat"}

# Get the path of the main file
def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Create a folder in the user/username directory
def get_recipes_directory():
    user_home = os.path.expanduser("~")  
    recipes_dir = os.path.join(user_home, 'MyAppRecipes')  
    return recipes_dir

# Get the useful paths
base_path = get_base_path()
icon_path = os.path.join(base_path, 'resources/Fork_Knife.ico')
im_dir = os.path.join(base_path, 'temp')
im_path = os.path.join(base_path, 'temp_image.png')
recipes_dir = get_recipes_directory()  
json_path = os.path.join(recipes_dir, 'recipes.json')

# Load JSON recipe file, and create it if it doesn't exist
def load_recipe():
    # For first use, create the directory
    if not os.path.exists(recipes_dir):
        os.makedirs(recipes_dir)  
        print(f"Created directory: {recipes_dir}")

    if os.path.exists(json_path):
        print(f"Loading recipes from: {json_path}")
        with open(json_path, 'r') as f:
            try:
                recipes = json.load(f)
                if isinstance(recipes, dict):
                    return recipes
                else:
                    messagebox.showerror("Error", "The file does not contain a dictionary.")
                    return {}
            except json.JSONDecodeError:
                messagebox.showerror("Error", "The file is corrupted or invalid.")
                return {}
    # If the file doesn't exist then it is created
    else:
        print(f"Creating new JSON file at: {json_path}")
        with open(json_path, 'w') as f:
            empty_recipes = {}
            json.dump(empty_recipes, f, indent=4)
            # messagebox.showinfo("Info", f"File not found, created a new one at: {json_path}")
        return empty_recipes
    
# Save the recipe into a JSON file
def save_recipes(recipes, file_path=json_path):
    with open(file_path, 'w') as f:
        json.dump(recipes, f, indent=4)

# Function to delete temporary files (temp image when opening a recipe)
def clean_temp_files():
    temp_files = [im_path]
    
    for temp_file in temp_files:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print(f"Temporary file {temp_file} deleted.")
            else:
                print(f"File {temp_file} not found.")
        except Exception as e:
            print(f"Error deleting file {temp_file}: {e}")

# Merge two colors to create a gradient of color
def create_gradient(canvas, color1, color2):
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    for i in range(height):
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        color = f'#{r:02x}{g:02x}{b:02x}' 
        canvas.create_line(0, i, width, i, fill=color)

# Convert color from hex to rgb
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Hover effect for buttons
def on_enter(e):
    e.widget['background'] = sage_green

def on_leave(e):
    e.widget['background'] = pale_blue