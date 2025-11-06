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

# Main function to run the ticket booking system
def main():
    f = pyfiglet.Figlet(font="slant")  
    print(f.renderText("WELCOME TO PY-TICKET"))
    username = get_verified_user()
    name, age, passenger_count = get_booking_details()
    seat_type = book_ticket(age)
    create_ticket(username, name, age, passenger_count, seat_type)


# Function to verify registered users
def get_verified_user():
    while True:
        username = get_input(prompt="Enter your PY-TICKET Username: ", required=True)
        if username not in registered_users:
            print("Not a registered user! ")
            continue
        return username


# Function to get booking details from the user
def get_booking_details():  
    print("ENTER YOUR BOOKING DETAILS HERE!")
    passenger_count = get_input(prompt="How many passengers would you like to book seats for? ", input_type="int", error_prompt="Not a valid passenger amount!")
    name=[]
    age=[]
    for i in range(passenger_count):
        print (f"\nPassenger {i+1}")
        name.append(get_input(prompt="Name: ", required=True))
        age.append(get_input(prompt="Age: ", required=True, input_type="int", error_prompt="Not a valid age!"))
    return (name, age, passenger_count)

# AGE-FILTER
# ADD ALGORITHM TO BOOK SEAT TYPE BASED ON AGE FILTERING
def book_ticket(a):  
    try:
        train = Train()
    except Exception:
        sys.exit("Error occured!")
    for age in a:
        if age > 60:
            status = train.book_lower()
            if status == "Full":
                print("All seats are booked! No seats available.")
                return None
            else: 
                return "Lower-seat"    
        elif 30 <= age <= 60:
            status = train.book_middle()
            if status == "Full":
                print("All seats are booked! No seats available.")
                return None
            else: 
                return "Middle-seat"
        else:
            status = train.book_upper()
            if status == "Full":
                print("All seats are booked! No seats available.")
                return None
            else:
                return "Upper-seat" 

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
def create_ticket(username, name, age, passenger_count, seat_type):  # only displays the latest passenger ticket in ticket.txt (save ticket data somewhere).
    for i in range(passenger_count):
        with open("ticket.txt", "w") as file:
            file.write(
                f"Ticket under : {username}\n Ticket Id: {id_genrator(seat_type)}\n Name: {name[i]}\n Age: {age[i]}\n Seat: {seat_type}"
            )


if __name__ == "__main__":
    main()
