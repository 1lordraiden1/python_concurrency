import threading
import time
import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

# JSON file paths
SEATS_FILE = "seats.json"
HISTORY_FILE = "booking_history.json"

# Initialize JSON files if they do not exist
def initialize_json_files():
    try:
        # Initialize seat data
        with open(SEATS_FILE, "x") as file:
            json.dump(["Available" for _ in range(10)], file)
    except FileExistsError:
        pass  # File already exists

    try:
        # Initialize booking history
        with open(HISTORY_FILE, "x") as file:
            json.dump([], file)
    except FileExistsError:
        pass  # File already exists

# Load seat availability from JSON
def load_seat_data():
    with open(SEATS_FILE, "r") as file:
        return json.load(file)

# Save updated seat availability to JSON
def save_seat_data(data):
    with open(SEATS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load booking history from JSON
def load_booking_history():
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)

# Save updated booking history to JSON
def save_booking_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Booking system
def book_seat(user_id, seat_number):
    """Function to book a seat for a user."""
    thread_id = threading.get_ident()
    start_time = datetime.now().isoformat()

    with seats_lock:
        seats = load_seat_data()
        if seat_number < 0 or seat_number >= len(seats):
            return "Invalid seat number"

        if seats[seat_number] == "Available":
            time.sleep(0.5)  # Simulate booking delay
            seats[seat_number] = f"Booked by User {user_id}"
            save_seat_data(seats)

            end_time = datetime.now().isoformat()
            history = load_booking_history()
            history.append({
                "user_id": user_id,
                "seat_number": seat_number,
                "start_time": start_time,
                "end_time": end_time,
                "thread_id": thread_id,
                "action": "booked"
            })
            save_booking_history(history)

            return "Booking successful"
        else:
            return "Seat already booked"

def cancel_seat(user_id, seat_number):
    """Function to cancel a booking."""
    thread_id = threading.get_ident()
    start_time = datetime.now().isoformat()

    with seats_lock:
        seats = load_seat_data()
        if seat_number < 0 or seat_number >= len(seats):
            return "Invalid seat number"

        if seats[seat_number] == f"Booked by User {user_id}":
            time.sleep(0.5)  # Simulate cancellation delay
            seats[seat_number] = "Available"
            save_seat_data(seats)

            end_time = datetime.now().isoformat()
            history = load_booking_history()
            history.append({
                "user_id": user_id,
                "seat_number": seat_number,
                "start_time": start_time,
                "end_time": end_time,
                "thread_id": thread_id,
                "action": "cancelled"
            })
            save_booking_history(history)

            return "Cancellation successful"
        else:
            return "Seat not booked by you"

def display_seat_availability():
    """Display the current seat availability."""
    seats = load_seat_data()
    print("\nCurrent Seat Availability:")
    for i, status in enumerate(seats):
        print(f"Seat {i}: {status}")
    print()

def update_gui_seat_availability():
    """Update the seat availability display in the GUI."""
    seats = load_seat_data()
    for i, seat_label in enumerate(seat_labels):
        seat_label.config(text=f"Seat {i}: {seats[i]}", fg="green" if seats[i] == "Available" else "red")

def gui_book_seat(user_id, seat_number):
    """GUI callback to book a seat."""
    result = book_seat(user_id, seat_number)
    messagebox.showinfo("Booking Result", result)
    update_gui_seat_availability()

def gui_cancel_seat(user_id, seat_number):
    """GUI callback to cancel a booking."""
    result = cancel_seat(user_id, seat_number)
    messagebox.showinfo("Cancellation Result", result)
    update_gui_seat_availability()

def view_booking_history():
    """Display all booking history in a new window."""
    history_window = tk.Toplevel(root)
    history_window.title("Booking History")

    history = load_booking_history()
    if history:
        for idx, entry in enumerate(history):
            tk.Label(
                history_window, 
                text=f"{idx + 1}. User {entry['user_id']} {entry['action']} Seat {entry['seat_number']} "
                     f"from {entry['start_time']} to {entry['end_time']} (Thread: {entry['thread_id']})", 
                font=("Arial", 12)
            ).pack(pady=2)
    else:
        tk.Label(history_window, text="No bookings yet.", font=("Arial", 12)).pack(pady=10)

# Create the GUI
root = tk.Tk()
root.title("Movie Ticket Booking System")

seats_lock = threading.Lock()
seat_labels = []

for i in range(10):  # Initialize GUI with 10 seats
    seat_label = tk.Label(root, text=f"Seat {i}: ", font=("Arial", 12), width=30, anchor="w")
    seat_label.grid(row=i, column=0, padx=10, pady=5)
    seat_labels.append(seat_label)

frame = tk.Frame(root)
frame.grid(row=10, column=0, padx=10, pady=10)

tk.Label(frame, text="User ID:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
user_id_entry = tk.Entry(frame, font=("Arial", 12))
user_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Seat Number:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
seat_number_entry = tk.Entry(frame, font=("Arial", 12))
seat_number_entry.grid(row=1, column=1, padx=5, pady=5)

def on_book_button_click():
    try:
        user_id = int(user_id_entry.get())
        seat_number = int(seat_number_entry.get())
        gui_book_seat(user_id, seat_number)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for User ID and Seat Number.")

def on_cancel_button_click():
    try:
        user_id = int(user_id_entry.get())
        seat_number = int(seat_number_entry.get())
        gui_cancel_seat(user_id, seat_number)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for User ID and Seat Number.")

book_button = tk.Button(frame, text="Book Seat", font=("Arial", 12), command=on_book_button_click)
book_button.grid(row=2, column=0, columnspan=2, pady=10)

cancel_button = tk.Button(frame, text="Cancel Booking", font=("Arial", 12), command=on_cancel_button_click)
cancel_button.grid(row=3, column=0, columnspan=2, pady=10)

history_button = tk.Button(frame, text="View Booking History", font=("Arial", 12), command=view_booking_history)
history_button.grid(row=4, column=0, columnspan=2, pady=10)

# Run the GUI
def run_gui():
    initialize_json_files()
    update_gui_seat_availability()
    root.mainloop()

if __name__ == "__main__":
    run_gui()
