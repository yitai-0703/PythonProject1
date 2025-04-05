# Apache Airlines Seat Booking System - Part A.4

# Constants for special seat types
AISLE = 'X'
STORAGE = 'S'
FREE = 'F'
RESERVED = 'R'

# Create seat map: 80 rows (1-80) x 6 columns (A-F, and X)
rows = 80
cols = ['A', 'B', 'C', 'X', 'D', 'E', 'F']
seat_map = {}

for row in range(1, rows + 1):
    for col in cols:
        # Define aisle and storage area manually (simplified example)
        if col in ['D', 'E', 'F'] and 78 >= row > 76:
            seat_map[f"{row}{col}"] = STORAGE
        elif col == 'X':
            seat_map[f"{row}{col}"] = AISLE
        else:
            seat_map[f"{row}{col}"] = FREE


# Helper functions
def check_seat_availability(seat):
    status = seat_map.get(seat)
    if status == FREE:
        print(f"Seat {seat} is available.")
    elif status == RESERVED:
        print(f"Seat {seat} is already reserved.")
    elif status in [AISLE, STORAGE]:
        print(f"Seat {seat} cannot be booked. It's marked as '{status}'.")
    else:
        print("Invalid seat number.")


def book_seat(seat):
    if seat not in seat_map:
        print("Invalid seat number.")
    elif seat_map[seat] == FREE:
        seat_map[seat] = RESERVED
        print(f"Seat {seat} has been successfully booked.")
    elif seat_map[seat] == RESERVED:
        print("That seat is already reserved.")
    else:
        print("That seat cannot be booked.")


def free_seat(seat):
    if seat not in seat_map:
        print("Invalid seat number.")
    elif seat_map[seat] == RESERVED:
        seat_map[seat] = FREE
        print(f"Seat {seat} is now available.")
    elif seat_map[seat] == FREE:
        print("That seat is already free.")
    else:
        print("That seat cannot be modified.")


def show_booking_status():
    print("\nCurrent Booking Status:")
    for row in range(1, rows + 1):
        status_row = []
        for col in cols:
            seat = f"{row}{col}"
            status_row.append(seat_map[seat])
        print(f"Row {row:02}: {status_row}")


# Main menu loop
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


# Run the program
if __name__ == "__main__":
    main_menu()