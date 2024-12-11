import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

# Function to run Python script for each number in a separate process
def run_script_for_number(number):
    try:
        # Use subprocess to run the script in a new process
        subprocess.Popen(['python', 'final_project.py', str(number)])
        print(f"Script running for project {number}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run script for {number}: {e}")

# Function to handle the user input
def on_submit():
    # Get the input from the text box
    input_numbers = entry.get()
    
    # Split input by commas, filter out non-numeric values
    numbers = [num.strip() for num in input_numbers.split(',') if num.strip().isdigit()]
    
    if not numbers:
        messagebox.showerror("Invalid Input", "Please enter valid numbers separated by commas.")
        return
    
    # Create and start a new thread for each number
    for number in numbers:
        thread = threading.Thread(target=run_script_for_number, args=(number,))
        thread.start()

# Setting up the Tkinter window
root = tk.Tk()
root.title("Run Projects for Numbers")

# Label
label = tk.Label(root, text="Enter numbers separated by commas:")
label.pack(pady=10)

# Entry box for numbers
entry = tk.Entry(root, width=40)
entry.pack(pady=10)

# Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()




