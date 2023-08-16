import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="F8DHAZS9",
    database="progresspulsedb"
)
cursor = conn.cursor()

# Create the main application window
root = tk.Tk()
root.title("ProgressPulse")

# Define functions for database operations
def add_workout():
    # Fetch data from the GUI fields
    user_id = user_id_var.get()
    date = date_var.get()
    workout_type = workout_type_var.get()
    duration = duration_var.get()

    # Insert data into Workouts table
    cursor.execute(
        "INSERT INTO Workouts (user_id, date, workout_type, duration) VALUES (%s, %s, %s, %s)",
        (user_id, date, workout_type, duration)
    )
    conn.commit()
    messagebox.showinfo("Success", "Workout added successfully!")

# Create GUI components
user_id_var = tk.StringVar()
date_var = tk.StringVar()
workout_type_var = tk.StringVar()
duration_var = tk.IntVar()

user_id_label = tk.Label(root, text="User ID:")
user_id_entry = tk.Entry(root, textvariable=user_id_var)

date_label = tk.Label(root, text="Date:")
date_entry = tk.Entry(root, textvariable=date_var)

workout_type_label = tk.Label(root, text="Workout Type:")
workout_type_entry = tk.Entry(root, textvariable=workout_type_var)

duration_label = tk.Label(root, text="Duration (minutes):")
duration_entry = tk.Entry(root, textvariable=duration_var)

add_button = tk.Button(root, text="Add Workout", command=add_workout)

# Layout GUI components
user_id_label.pack()
user_id_entry.pack()

date_label.pack()
date_entry.pack()

workout_type_label.pack()
workout_type_entry.pack()

duration_label.pack()
duration_entry.pack()

add_button.pack()

# Start the GUI event loop
root.mainloop()

# Close the database connection
conn.close()