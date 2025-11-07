import pyfiglet
from my_utilities.my_functions import get_input
import json
from pathlib import Path
import random 
import sys

registered_users = ["User_1", "User_2"]

def get_json_data_path(file):
    BASE_DIR = Path(__file__).resolve().parent
    if file == "train_seats_count":
        return BASE_DIR / "data" / "train_seats_count.json"
    elif file == "train_seat_number":
        return BASE_DIR / "data" / "train_seat_number.json"
    else:
        raise ValueError(f"Invalid file key: {file}. Expected 'train_seats_count' or 'train_seat_number'.")

# Train class to handle seat bookings
class Train:
    def __init__(self):
        self._train_seats_data = get_json_data_path(file="train_seats_count")
        if self._train_seats_data.exists():
            with open(self._train_seats_data,"r") as data:
                self.seats_data = json.load(data) 
        else:
            with open(self._train_seats_data,"w") as data:
                json.dump({"seats": {"upper_seats": 27, "lower_seats": 27, "middle_seats": 18 }}, data, indent=4)
            with open(self._train_seats_data,"r") as data:
                self.seats_data = json.load(data)

    def book_lower(self):
        if self.seats_data["seats"]["lower_seats"] > 0:
            self.seats_data["seats"]["lower_seats"] -= 1
            with open(self._train_seats_data,"w") as file:
                json.dump(self.seats_data, file, indent=4)
            print("Lower seat booked successfully!")
        else:
            status = self.book_middle()
            return status

    def book_upper(self):
        if self.seats_data["seats"]["upper_seats"] > 0:
            self.seats_data["seats"]["upper_seats"] -= 1
            with open(self._train_seats_data,"w") as file:
                json.dump(self.seats_data, file, indent=4)
            print("Upper seat booked successfully!")
        elif self.seats_data["seats"]["upper_seats"] + self.seats_data["seats"]["middle_seats"] + self.seats_data["seats"]["lower_seats"] > 0:
            if self.seats_data["seats"]["middle_seats"] > 0:
                self.book_middle()
            elif self.seats_data["seats"]["lower_seats"]:
                self.book_lower()
        else:
            return "Full"

    def book_middle(self):
        if self.seats_data["seats"]["middle_seats"] > 0:
            self.seats_data["seats"]["middle_seats"] -= 1
            with open(self._train_seats_data,"w") as file:
                json.dump(self.seats_data, file, indent=4)
            print("Middle seat booked successfully!")
        else:
            status = self.book_upper()
            return status
        

#seat number data structure
def assign_seat_number(seat_type):
    train_seat_number = get_json_data_path(file="train_seat_number")
    seat_number_array = {}
    with open(train_seat_number,"r") as seat_number_data:
        seat_number_array = json.load(seat_number_data)
        if seat_type == "Lower-seat":
                seat_number = seat_number_array["seat_number"]["lower_seat_number"].pop(0)
        elif seat_type == "Middle-seat":
            seat_number = seat_number_array["seat_number"]["middle_seat_number"].pop(0)
        else:
            seat_number = seat_number_array["seat_number"]["upper_seat_number"].pop(0)
    with open(train_seat_number,"w") as seat_number_file:
        json.dump(seat_number_array, seat_number_file, indent=4)
    return seat_number


# Main function to run the ticket booking system
def main():
    f = pyfiglet.Figlet(font="slant")  
    print(f.renderText("WELCOME TO PY-TICKET"))
    username = get_verified_user()
    passenger_count = get_input(prompt="How many passengers would you like to book seats for? ", input_type="int", error_prompt="Not a valid passenger amount!")
    book_ticket(username, passenger_count)



# Function to verify registered users
def get_verified_user():
    while True:
        username = get_input(prompt="Enter your PY-TICKET Username: ", required=True)
        if username not in registered_users:
            print("Not a registered user! ")
            continue
        return username


# Function to get booking details from the user
def get_booking_details(i):  
    print(f"ENTER YOUR BOOKING DETAILS HERE FOR PASSENGER {i+1}:")
    name = get_input(prompt="Name: ", required=True)
    age = get_input(prompt="Age: ", required=True, input_type="int", error_prompt="Not a valid age!")
    return (name, age)

# AGE-FILTER
# ADD ALGORITHM TO BOOK SEAT TYPE BASED ON AGE FILTERING
def book_ticket(username, passenger_count):
    for i in range(passenger_count):
        name, age = get_booking_details(i)
        try:
            train = Train()
        except Exception:
            sys.exit("Error occured!")
        if age > 60:
            status = train.book_lower()
            if status == "Full":
                print("All seats are booked! No seats available.")
                return None
            else: 
                seat_type = "Lower-seat"    
        elif 30 <= age <= 60:
            status = train.book_middle()
            if status == "Full":
                print("All seats are booked! No seats available.")
                return None
            else: 
                seat_type = "Middle-seat"
        else:
            status = train.book_upper()
            if status == "Full":
                print("All seats are booked! No seats available.")
                return None
            else:
                seat_type = "Upper-seat" 
        create_ticket(username, name, age, seat_type)

# ID Genrator
def id_genrator(seat_type):
    if seat_type == "Lower-seat":
        seat_code = "L"
    elif seat_type == "Middle-seat":
        seat_code = "M"
    else:
        seat_code = "U"
    return f"{seat_code}-{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNPQRSTUVWXYZ')}{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNPQRSTUVWXYZ')}"


# Function to create and save the ticket details
def create_ticket(username, name, age, seat_type):  # only displays the latest passenger ticket in ticket.txt (save ticket data somewhere).
    with open("ticket1.txt", "a") as file:
        file.write(
            f"Ticket under : {username}\n Ticket Id: {id_genrator(seat_type)}\n Name: {name}\n Age: {age}\n Seat:{assign_seat_number(seat_type)} {seat_type}\n"
        )


if __name__ == "__main__":
    main()
