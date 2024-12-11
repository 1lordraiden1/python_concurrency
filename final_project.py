import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

# JSON file paths
SEATS_FILE = "seats.json"
HISTORY_FILE = "booking_history.json"

# Initialize JSON files if they do not exist
def initialize_json_files():
    try:
        with open(SEATS_FILE, "x") as file:
            json.dump(["Available" for _ in range(10)], file)
    except FileExistsError:
        pass

    try:
        with open(HISTORY_FILE, "x") as file:
            json.dump([], file)
    except FileExistsError:
        pass

# Load seat data
def load_seat_data():
    with open(SEATS_FILE, "r") as file:
        return json.load(file)

# Save seat data
def save_seat_data(data):
    with open(SEATS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load booking history
def load_booking_history():
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)

# Save booking history
def save_booking_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Booking system
def book_seat(user_id, seat_number):
    thread_id = threading.get_ident()
    start_time = datetime.now().isoformat()

    with seats_lock:
        seats = load_seat_data()
        if seat_number < 0 or seat_number >= len(seats):
            return "Invalid seat number"

        if seats[seat_number] == "Available":
            time.sleep(0.5)
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
    thread_id = threading.get_ident()
    start_time = datetime.now().isoformat()

    with seats_lock:
        seats = load_seat_data()
        if seat_number < 0 or seat_number >= len(seats):
            return "Invalid seat number"
        
        if seats[seat_number] == "Available":
            return "Already not booked"

        if seats[seat_number] == f"Booked by User {user_id}":
            time.sleep(0.5)
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

def gui_cancel_seat(user_id, seat_number):
    """GUI callback to cancel a booking."""
    result = cancel_seat(user_id, seat_number)
    messagebox.showinfo("Cancellation Result", result)
    update_gui_seat_availability()
    
def clear_all_bookings():
    """Admin function to clear all bookings."""
    with seats_lock:
        seats = ["Available" for _ in range(10)]
        save_seat_data(seats)
        history = load_booking_history()
        history.append({
            "user_id": "admin",
            "seat_number": "all",
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "thread_id": threading.get_ident(),
            "action": "cleared all bookings"
        })
        save_booking_history(history)
        update_gui_seat_availability()
        return "All bookings cleared!"

# GUI Functions
def update_gui_seat_availability():
    """Update the seat availability display in the GUI."""
    seats = load_seat_data()
    for i, seat_label in enumerate(seat_labels):
        seat_label.config(text=f"Seat {i}: {seats[i]}", fg="green" if seats[i] == "Available" else "red")

def view_admin_history():
    """Admin view for booking history."""
    history = load_booking_history()
    admin_history_window = tk.Toplevel(root)
    admin_history_window.title("Admin: Booking History")
    admin_history_window.geometry("600x400")

    text_widget = tk.Text(admin_history_window, font=("Arial", 12), wrap=tk.WORD)
    text_widget.pack(expand=True, fill=tk.BOTH)
    if history:
        for entry in history:
            text_widget.insert(
                tk.END,
                f"User {entry['user_id']} {entry['action']} Seat {entry['seat_number']} "
                f"at {entry['start_time']} (Thread ID: {entry['thread_id']})\n"
            )
    else:
        text_widget.insert(tk.END, "No history available.\n")

# UI Enhancements
def create_tabbed_interface():
    tab_control = ttk.Notebook(root)

    # User tab
    user_tab = ttk.Frame(tab_control)
    tab_control.add(user_tab, text="User Panel")
    create_user_panel(user_tab)

    # Admin tab
    admin_tab = ttk.Frame(tab_control)
    tab_control.add(admin_tab, text="Admin Panel")
    create_admin_panel(admin_tab)

    tab_control.pack(expand=1, fill="both")

def create_user_panel(frame):
    global seat_labels
    seat_labels.clear()

    for i in range(10):
        seat_label = tk.Label(frame, text=f"Seat {i}: ", font=("Arial", 12), width=30, anchor="w")
        seat_label.grid(row=i, column=0, padx=10, pady=5)
        seat_labels.append(seat_label)

    controls_frame = tk.Frame(frame)
    controls_frame.grid(row=11, column=0, padx=10, pady=10)

    tk.Label(controls_frame, text="User ID:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    user_id_entry = tk.Entry(controls_frame, font=("Arial", 12))
    user_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(controls_frame, text="Seat Number:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
    seat_number_entry = tk.Entry(controls_frame, font=("Arial", 12))
    seat_number_entry.grid(row=1, column=1, padx=5, pady=5)

    def on_book_button_click():
        try:
            user_id = int(user_id_entry.get())
            seat_number = int(seat_number_entry.get())
            result = book_seat(user_id, seat_number)
            messagebox.showinfo("Booking Result", result)
            update_gui_seat_availability()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for User ID and Seat Number.")

    def on_cancel_button_click():
        try:
            user_id = int(user_id_entry.get())
            seat_number = int(seat_number_entry.get())
            gui_cancel_seat(user_id, seat_number)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for User ID and Seat Number.")
    book_button = tk.Button(controls_frame, text="Book Seat", font=("Arial", 12), command=on_book_button_click)
    book_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    cancel_button = tk.Button(frame, text="Cancel Booking", font=("Arial", 12), command=on_cancel_button_click)
    cancel_button.grid(row=13, column=0, columnspan=2, pady=10)

def create_admin_panel(frame):
    clear_button = tk.Button(frame, text="Clear All Bookings", font=("Arial", 12), command=lambda: messagebox.showinfo("Admin Action", clear_all_bookings()))
    clear_button.grid(row=0, column=0, padx=10, pady=10)

    history_button = tk.Button(frame, text="View Booking History", font=("Arial", 12), command=view_admin_history)
    history_button.grid(row=1, column=0, padx=10, pady=10)

# Main function
if __name__ == "__main__":
    initialize_json_files()

    root = tk.Tk()
    root.title("Movie Ticket Booking System")
    root.geometry("800x600")

    seats_lock = threading.Lock()
    seat_labels = []

    create_tabbed_interface()
    update_gui_seat_availability()

    root.mainloop()
