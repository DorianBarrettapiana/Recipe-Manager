# Recipe Manager - Python Application

This project is a recipe management application developed in Python using Tkinter for the graphical interface and JSON for data storage. It allows users to create, manage, and import/export to share recipes. The application includes features like ingredient and step management, difficulty and price rating, and encoding images in Base64 format to store them in a JSON file.

## Features

- **Add Recipes**: Create new recipes with name, ingredients, steps, difficulty, price, and an image.
- **Import/Export Recipes**: Share your recipes with friends by exporting them to a JSON file, which can be imported by others.
- **Image Encoding**: Encode images in Base64 and store them in the JSON file to keep everything in a single file.
- **Recipe Management**: View and edit. You can also sort recipes by difficulty or price.

## Requirements

- Python 3.7 or higher
- Tkinter (comes pre-installed with Python)
- `base64` for image encoding (part of Python's standard library)
- pyInstaller (or auto-py-to-exe) for compilation (optional)

## Installation

1. **Clone the repository:**

   Open your terminal and run the following command:

   ```bash
   git clone https://github.com/Nayrhode/recipe-manager.git
   cd recipe-manager

2. **exe compilation:**

   You can compile it using pyInstaller:

   ```bash
   pyinstaller --onedir --windowed --add-data "resources;resources" main.py

