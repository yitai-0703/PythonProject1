# Apache Airlines Seat Booking System - Part B.2 (with Database Integration)

import sqlite3
import random
import string

# Constants for special seat types
AISLE = 'X'
STORAGE = 'S'
FREE = 'F'
RESERVED = 'R'

# Create seat map: 80 rows (1-80) x 6 columns (A-F and X)
rows = 80
cols = ['A', 'B', 'C', 'X', 'D', 'E', 'F']
seat_map = {}

for row in range(1, rows + 1):
    for col in cols:
        if col in ['D', 'E', 'F'] and 78 >= row > 76:
            seat_map[f"{row}{col}"] = STORAGE
        elif col == 'X':
            seat_map[f"{row}{col}"] = AISLE
        else:
            seat_map[f"{row}{col}"] = FREE

# Initialize SQLite database
conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    reference TEXT PRIMARY KEY,
    passport_number TEXT,
    first_name TEXT,
    last_name TEXT,
    seat TEXT
)
''')
conn.commit()

# Helper: Generate unique 8-char booking reference
existing_refs = set()

def generate_booking_reference():
    while True:
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if ref not in existing_refs:
            existing_refs.add(ref)
            return ref

# Check availability
def check_seat_availability(seat):
    status = seat_map.get(seat)
    if status == FREE:
        print(f"Seat {seat} is available.")
    elif status in [AISLE, STORAGE]:
        print(f"Seat {seat} cannot be booked. It's marked as '{status}'.")
    elif status != FREE and status != None:
        print(f"Seat {seat} is reserved with reference {status}.")
    else:
        print("Invalid seat number.")

# Book seat
def book_seat(seat):
    if seat not in seat_map:
        print("Invalid seat number.")
        return
    if seat_map[seat] != FREE:
        print("Seat cannot be booked.")
        return

    passport = input("Enter passport number: ")
    first = input("Enter first name: ")
    last = input("Enter last name: ")

    ref = generate_booking_reference()
    seat_map[seat] = ref
    cursor.execute("INSERT INTO bookings VALUES (?, ?, ?, ?, ?)",
                   (ref, passport, first, last, seat))
    conn.commit()
    print(f"Seat {seat} successfully booked with reference {ref}.")

# Free seat
def free_seat(seat):
    if seat not in seat_map:
        print("Invalid seat number.")
        return
    status = seat_map[seat]
    if status == FREE:
        print("That seat is already free.")
    elif status in [AISLE, STORAGE]:
        print("That seat cannot be modified.")
    else:
        cursor.execute("DELETE FROM bookings WHERE reference = ?", (status,))
        conn.commit()
        seat_map[seat] = FREE
        print(f"Seat {seat} has been freed and booking {status} deleted.")

# Show full status
def show_booking_status():
    print("\nCurrent Booking Status:")
    for row in range(1, rows + 1):
        status_row = []
        for col in cols:
            seat = f"{row}{col}"
            status = seat_map[seat]
            status_row.append(status if status in [FREE, AISLE, STORAGE] else 'R')
        print(f"Row {row:02}: {status_row}")

# Main loop
def main_menu():
    while True:
        print("\nApache Airlines Seat Booking System")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            seat = input("Enter seat (e.g., 12B): ").upper()
            check_seat_availability(seat)
        elif choice == '2':
            seat = input("Enter seat to book: ").upper()
            book_seat(seat)
        elif choice == '3':
            seat = input("Enter seat to free: ").upper()
            free_seat(seat)
        elif choice == '4':
            show_booking_status()
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid option. Please select 1-5.")

# Run program
if __name__ == "__main__":
    main_menu()
    conn.close()
