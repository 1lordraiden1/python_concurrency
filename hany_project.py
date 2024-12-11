import streamlit as st
import threading
import time
import json
from datetime import datetime

# ========================
# Database and Logs Simulation (File-based)
# ========================

DATABASE_FILE = 'seats.json'
THREAD_LOG_FILE = 'thread_logs.json'

def initialize_database():
    """ Initialize the seat database. """
    initial_data = {"seats": {f"seat_{i}": "available" for i in range(1, 21)}}  # 20 seats
    with open(DATABASE_FILE, 'w') as file:
        json.dump(initial_data, file)

def load_seat_data():
    """ Load seat data from the file. """
    with open(DATABASE_FILE, 'r') as file:
        return json.load(file)

def save_seat_data(data):
    """ Save updated seat data to the file. """
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file)

def initialize_thread_logs():
    """ Initialize the thread logs file. """
    with open(THREAD_LOG_FILE, 'w') as file:
        json.dump({}, file)

def load_thread_logs():
    """ Load thread logs from the file. """
    try:
        with open(THREAD_LOG_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        initialize_thread_logs()
        return {}

def save_thread_logs(logs):
    """ Save thread logs to the file. """
    with open(THREAD_LOG_FILE, 'w') as file:
        json.dump(logs, file)

# ========================
# Thread-safe Seat Booking System
# ========================

class SeatBookingSystem:
    def __init__(self):
        self.lock = threading.Lock()

    def book_seat(self, seat_id, user_name):
        """ Attempt to book a seat. """
        thread_id = threading.current_thread().name
        log_thread_start(thread_id)

        with self.lock:
            seat_data = load_seat_data()
            if seat_data['seats'][seat_id] == 'available':
                seat_data['seats'][seat_id] = user_name
                save_seat_data(seat_data)
                log_thread_end(thread_id)
                return True  # Booking successful
            else:
                log_thread_end(thread_id)
                return False  # Seat is already booked

    def get_seat_status(self):
        """ Return the current status of all seats. """
        with self.lock:
            return load_seat_data()['seats']

# ========================
# Helper Functions for Thread Logging
# ========================

def log_thread_start(thread_id):
    """ Log thread start time and status in the log file. """
    logs = load_thread_logs()
    logs[thread_id] = {
        "name" : thread_id,
        "status": "Running",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": None
    }
    save_thread_logs(logs)

def log_thread_end(thread_id):
    """ Log thread end time and status in the log file. """
    logs = load_thread_logs()
    if thread_id in logs:
        logs[thread_id]["status"] = "Completed"
        logs[thread_id]["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_thread_logs(logs)

# ========================
# Streamlit GUI
# ========================

st.title("🎟️ Movie Ticket Booking System")
st.write("Book your seat for the movie. Avoid double booking and experience a live dynamic seat update.")

# Initialize database and thread logs if they do not exist
try:
    load_seat_data()
except FileNotFoundError:
    initialize_database()

try:
    load_thread_logs()
except FileNotFoundError:
    initialize_thread_logs()

# Create an instance of the SeatBookingSystem
booking_system = SeatBookingSystem()

# Sidebar Navigation
page = st.sidebar.selectbox("Navigation", ["Booking Page", "Admin Page", "Thread Activity"])

if page == "Booking Page":
    # Display current seat status
    st.subheader("Available Seats")
    seats = booking_system.get_seat_status()

    # Display seats in a grid layout
    columns = st.columns(5)  # 5 seats per row
    for i, (seat_id, status) in enumerate(seats.items()):
        col = columns[i % 5]
        if status == 'available':
            if col.button(f"{seat_id}", key=seat_id):
                st.session_state['selected_seat'] = seat_id
        else:
            col.write(f"{seat_id} ({status})")

    st.subheader("Book Your Seat")
    selected_seat = st.selectbox("Select a Seat", options=[seat for seat, status in seats.items() if status == 'available'])
    user_name = st.text_input("Enter your name")

    if st.button("Book Now"):
        if user_name and selected_seat:
            booking_success = booking_system.book_seat(selected_seat, user_name)
            if booking_success:
                st.success(f"Successfully booked {selected_seat} for {user_name}!")
            else:
                st.error(f"Seat {selected_seat} is already booked. Please select another seat.")
        else:
            st.warning("Please enter your name and select a seat to book.")
elif page == "Admin Page":
    st.title("🔧 Admin Dashboard")
    st.write("Manage seat bookings and view seat status.")
    seat_data = load_seat_data()
    booked_seats = {seat: user for seat, user in seat_data['seats'].items() if user != 'available'}
    available_seats = {seat: user for seat, user in seat_data['seats'].items() if user == 'available'}

    st.subheader("Booked Seats")
    if booked_seats:
        for seat, user in booked_seats.items():
            st.write(f"{seat}: Booked by {user}")
    else:
        st.write("No seats are currently booked.")
    st.subheader("Available Seats")
    st.write(", ".join(available_seats.keys()) if available_seats else "No seats are currently available.")

    # Button to reset all seats
    if st.button("Reset All Seats"):
        initialize_database()
        st.success("All seats have been reset to available.")
        st.experimental_rerun()

elif page == "Thread Activity":
    st.title("🧵 Thread Activity Dashboard")
    st.write("View the status and activity of all threads.")

    thread_logs = load_thread_logs()
    if thread_logs:
        for thread_id, info in thread_logs.items():
            st.write(f"Thread {thread_id}:")
            st.write(f"- Status: {info['status']}")
            st.write(f"- Start Time: {info['start_time']}")
            st.write(f"- End Time: {info['end_time']}")
            st.write("---")
    else:
        st.write("No thread activity recorded yet.")
