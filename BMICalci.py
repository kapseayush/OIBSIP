import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime

# Initialize user data storage
user_data_file = 'user_data.json'


def load_user_data():
    try:
        with open(user_data_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_user_data(data):
    with open(user_data_file, 'w') as file:
        json.dump(data, file, indent=4)


# Load existing data
user_data = load_user_data()


# BMI Calculation and Category
def calculate_bmi(weight, height):
    return weight / (height ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


def submit_data():
    try:
        user = user_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive numbers.")

        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if user not in user_data:
            user_data[user] = []

        user_data[user].append({
            'timestamp': timestamp,
            'weight': weight,
            'height': height,
            'bmi': bmi,
            'category': category
        })

        save_user_data(user_data)

        result_label.config(text=f"Your BMI is: {bmi:.2f}\nCategory: {category}")
        messagebox.showinfo("Data Saved", "Your data has been saved successfully!")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


def show_trends():
    user = user_entry.get()
    if user not in user_data:
        messagebox.showerror("No Data", "No data found for this user.")
        return

    dates = [entry['timestamp'] for entry in user_data[user]]
    bmis = [entry['bmi'] for entry in user_data[user]]

    fig, ax = plt.subplots()
    ax.plot(dates, bmis, marker='o', linestyle='-')
    ax.set_title('BMI Trend Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('BMI')
    ax.grid(True)

    for tick in ax.get_xticklabels():
        tick.set_rotation(45)

    trend_window = tk.Toplevel(root)
    trend_window.title("BMI Trend Analysis")
    canvas = FigureCanvasTkAgg(fig, master=trend_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)


# Create the main window
root = tk.Tk()
root.title("BMI Calculator")

# Create and place widgets
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
user_entry = tk.Entry(root)
user_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=5)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Height (m):").grid(row=2, column=0, padx=10, pady=5)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=5)

submit_button = tk.Button(root, text="Calculate BMI", command=submit_data)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

trends_button = tk.Button(root, text="Show Trends", command=show_trends)
trends_button.grid(row=5, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
