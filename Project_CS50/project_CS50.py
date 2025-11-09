import pyfiglet
from my_utilities.my_functions import get_input
import json
from pathlib import Path
import random 

registered_users = ["User_1", "User_2"]

LOWER = "Lower-seat"
MIDDLE = "Middle-seat"
UPPER = "Upper-seat"

def get_json_data_path(file):
    BASE_DIR = Path(__file__).resolve().parent
    if file == "train_seats_count":
        return BASE_DIR / "data" / "train_seats_count.json"
    elif file == "train_seat_number":
        return BASE_DIR / "data" / "train_seat_number.json"
    elif file == "booking_chart":
        return BASE_DIR / "data" / "booking_chart.json"
    else:
        raise ValueError(f"Invalid file key: {file}. Expected 'train_seats_count' or 'train_seat_number'.")

# Train class to handle seat bookings
class Train:
    def __init__(self):
        self._train_seats_data = get_json_data_path("train_seats_count")
        if not self._train_seats_data.exists():
            with open(self._train_seats_data, "w") as file:
                json.dump({"seats": {"upper_seats": 27, "lower_seats": 27, "middle_seats": 18}}, file, indent=4)

        with open(self._train_seats_data, "r") as data:
            self.seats_data = json.load(data)

    def save(self):
        with open(self._train_seats_data, "w") as file:
            json.dump(self.seats_data, file, indent=4)

    def book_lower(self):
        if self.seats_data["seats"]["lower_seats"] > 0:
            self.seats_data["seats"]["lower_seats"] -= 1
            self.save()
            print("Lower seat booked successfully!")
            return LOWER
        else:
            return self.book_middle()

    def book_middle(self):
        if self.seats_data["seats"]["middle_seats"] > 0:
            self.seats_data["seats"]["middle_seats"] -= 1
            self.save()
            print("Middle seat booked successfully!")
            return MIDDLE
        else:
            return self.book_upper()

    def book_upper(self):
        if self.seats_data["seats"]["upper_seats"] > 0:
            self.seats_data["seats"]["upper_seats"] -= 1
            self.save()
            print("Upper seat booked successfully!")
            return UPPER
        elif (
            self.seats_data["seats"]["upper_seats"]
            + self.seats_data["seats"]["middle_seats"]
            + self.seats_data["seats"]["lower_seats"]
            == 0
        ):
            print("All seats are booked! No seats available.")
            return None
        else:
            if self.seats_data["seats"]["middle_seats"] > 0:
                return self.book_middle()
            elif self.seats_data["seats"]["lower_seats"] > 0:
                return self.book_lower()


# Main function to run the ticket booking system
def main():
    f = pyfiglet.Figlet(font="slant")  
    print(f.renderText("WELCOME TO PY-TICKET"))
    username = get_verified_user()
    passenger_count = get_input(prompt="How many passengers would you like to book seats for? ", input_type="int", error_prompt="Not a valid passenger amount!")
    book_ticket(username, passenger_count)


#seat number data structure
def assign_seat_number(seat_type):
    train_seat_number = get_json_data_path(file="train_seat_number")
    with open(train_seat_number,"r") as seat_number_data:
        seat_number_array = json.load(seat_number_data)
    try:    
        if seat_type == LOWER :
                seat_number = seat_number_array["seat_number"]["lower_seat_number"].pop(0)
        elif seat_type == MIDDLE:
            seat_number = seat_number_array["seat_number"]["middle_seat_number"].pop(0)
        elif seat_type == UPPER:
            seat_number = seat_number_array["seat_number"]["upper_seat_number"].pop(0)
        else:
            return None
    except IndexError:
        return None

    with open(train_seat_number,"w") as seat_number_file:
        json.dump(seat_number_array, seat_number_file, indent=4)
    return seat_number
    
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
    print(f"\nENTER YOUR BOOKING DETAILS HERE FOR PASSENGER {i+1}:")
    name = get_input(prompt="Name: ", required=True)
    age = get_input(prompt="Age: ", required=True, input_type="int", error_prompt="Not a valid age!")
    return (name, age)

# AGE-FILTER
# ADD ALGORITHM TO BOOK SEAT TYPE BASED ON AGE FILTERING
def book_ticket(username, passenger_count):
    train = Train()
    with open("ticket.txt","w") as file:
        pass
    for i in range(passenger_count):
        name, age = get_booking_details(i)
        if age > 60:
            seat_type = train.book_lower()
        elif 30 <= age <= 60:
            seat_type = train.book_middle()
        else:
            seat_type = train.book_upper()
        if not seat_type:
            return None
        create_ticket(username, name, age, seat_type)

# ID Genrator
def id_genrator(seat_type):
    if seat_type != None:
        seat_code = seat_type[0]
    else:
        return None
    return f"{seat_code}-{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNPQRSTUVWXYZ')}{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNPQRSTUVWXYZ')}"


# Function to create and save the ticket details
def create_ticket(username, name, age, seat_type):  
    if seat_type != None:
        seat_number = assign_seat_number(seat_type)
        id = id_genrator(seat_type)
    else:
        return None
    with open("ticket.txt", "a") as file:   
        file.write(
            f"Ticket under : {username}\n Ticket Id: {id}\n Name: {name}\n Age: {age}\n Seat:{seat_number} {seat_type}\n\n"
        )
    create_booking_chart(username, id, name, age, seat_type, seat_number)

#CREATE A BOOKING CHART TO DISPLAY ALL PASSENGERS IN THE TRAIN (JSON FILE)
def create_booking_chart(username, id, name, age, seat_type, seat_number):
    new_booking = {
        "username": username,
        "ticket_id": id,
        "name": name,
        "age": age,
        "seat_number": seat_number,
        "seat_type": seat_type
        },
    booking_chart_path = get_json_data_path("booking_chart")
    if not booking_chart_path.exists():
        with open(booking_chart_path, "w") as file:
            json.dump({"bookings": []}, file, indent=4)
    with open(get_json_data_path("booking_chart"), 'r') as file:
        ticket_details = json.load(file)
    ticket_details["bookings"].append(new_booking)
    booking_chart_path = get_json_data_path("booking_chart")
    with open(booking_chart_path, 'w') as file:
        json.dump(ticket_details,file, indent ='\t')


if __name__ == "__main__":
    main()
