import tkinter as tk
from tkinter import messagebox

def calculate_bmi(weight_entry, height_entry, bmi_label, category_label):
    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())
        height_m = height_cm / 100  # Convert height from centimeters to meters
        bmi = weight / (height_m * height_m)
        bmi_label.config(text="BMI: {:.2f}".format(bmi), fg=get_bmi_color(bmi), font=("Helvetica", 12, "bold"))
        category = classify_bmi(bmi)
        category_label.config(text="Category: {}".format(category), fg=get_category_color(category), font=("Helvetica", 12, "bold"))
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for weight and height.")

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_bmi_color(bmi):
    if bmi < 18.5:
        return "#2196F3"  # Blue
    elif 18.5 <= bmi < 25:
        return "#4CAF50"  # Green
    elif 25 <= bmi < 30:
        return "#FFC107"  # Orange
    else:
        return "#F44336"  # Red

def get_category_color(category):
    if category == "Underweight":
        return "#2196F3"  # Blue
    elif category == "Normal":
        return "#4CAF50"  # Green
    elif category == "Overweight":
        return "#FFC107"  # Orange
    else:
        return "#F44336"  # Red

# Create main window
root = tk.Tk()
root.title("BMI Calculator")

# Set background color
root.configure(bg="#f0f0f0")

# Create labels and entry fields
weight_label = tk.Label(root, text="Weight (kg):", bg="#f0f0f0", font=("Helvetica", 12))
weight_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
weight_entry = tk.Entry(root, font=("Helvetica", 12))
weight_entry.grid(row=0, column=1, padx=10, pady=5)

height_label = tk.Label(root, text="Height (cm):", bg="#f0f0f0", font=("Helvetica", 12))
height_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
height_entry = tk.Entry(root, font=("Helvetica", 12))
height_entry.grid(row=1, column=1, padx=10, pady=5)

calculate_button = tk.Button(root, text="Calculate BMI", command=lambda: calculate_bmi(weight_entry, height_entry, bmi_label, category_label), bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

bmi_label = tk.Label(root, text="", bg="#f0f0f0", font=("Helvetica", 16))
bmi_label.grid(row=3, column=0, columnspan=2)

category_label = tk.Label(root, text="", bg="#f0f0f0", font=("Helvetica", 16))
category_label.grid(row=4, column=0, columnspan=2)

# Run the main event loop
root.mainloop()
