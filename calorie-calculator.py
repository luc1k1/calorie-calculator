import tkinter as tk
from tkinter import messagebox
import requests
import json

# Load local fallback data
def load_local_data():
    try:
        with open("local_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

local_data = load_local_data()

# Function to search for calories
def search_calories():
    product_name = entry.get().strip().lower()
    if not product_name:
        messagebox.showwarning("Error", "Please enter a product name!")
        return

    # Check local data first
    if product_name in local_data:
        product = local_data[product_name]
        result_label.config(
            text=f"Calories: {product['calories']} kcal\n"
                 f"Protein: {product['protein']} g\n"
                 f"Fats: {product['fats']} g\n"
                 f"Carbs: {product['carbs']} g"
        )
        return

    # Query OpenFoodFacts API
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&json=1"
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("Error", "Failed to connect to the API. Check your internet connection.")
        return

    data = response.json()
    products = data.get("products", [])
    if not products:
        messagebox.showinfo("Result", f"No products found for '{product_name}'.")
        return

    # Get the first product from the API results
    product = products[0]
    nutrients = product.get("nutriments", {})

    # Fetch values or show "Data not available"
    calories = nutrients.get("energy-kcal_100g", "Data not available")
    protein = nutrients.get("proteins_100g", "Data not available")
    fats = nutrients.get("fat_100g", "Data not available")
    carbs = nutrients.get("carbohydrates_100g", "Data not available")

    result_label.config(
        text=f"Calories: {calories} kcal\nProtein: {protein} g\nFats: {fats} g\nCarbs: {carbs} g"
    )

# Function to clear the input and output
def clear_fields():
    entry.delete(0, tk.END)
    result_label.config(text="")

# Tkinter GUI setup
window = tk.Tk()
window.title("Calorie Calculator")

# Input field
tk.Label(window, text="Enter the product name:").pack(pady=5)
entry = tk.Entry(window, width=30)
entry.pack(pady=5)

# Buttons
tk.Button(window, text="Search", command=search_calories).pack(pady=5)
tk.Button(window, text="Clear", command=clear_fields).pack(pady=5)

# Result display
result_label = tk.Label(window, text="", font=("Arial", 12), justify=tk.LEFT)
result_label.pack(pady=10)

window.mainloop()
