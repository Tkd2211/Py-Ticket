import json
from pathlib import Path
import random
from my_utilities.my_functions import get_input
from cli_art import print_map, welcome_msg
from sys import exit

# Total fair collected this session
fair = 0

# Registered User list
registered_users = ["User_1", "User_2","User_3"]

# Constants used frequently in the file
LOWER = "Lower-seat"
MIDDLE = "Middle-seat"
UPPER = "Upper-seat"

# Gets the file path of the different json files in the data directory
def get_json_data_path(file):
    BASE_DIR = Path(__file__).resolve().parent
    if file == "train_seats_count":
        return BASE_DIR / "data" / "train_seats_count.json"
    elif file == "train_seat_number":
        return BASE_DIR / "data" / "train_seat_number.json"
    elif file == "booking_chart":
        return BASE_DIR / "data" / "booking_chart.json"
    else:
        raise ValueError(
            f"Invalid file key: {file}. Expected 'train_seats_count' or 'train_seat_number'."
        )

# Loads json file into a variable to manipulate data stored inside the json file.
def load_json(file):
    BASE_DIR = Path(__file__).resolve().parent
    if file == "train_seats_count":
        file_path = BASE_DIR / "data" / "train_seats_count.json"
        if not file_path.exists():
            with open(file_path, "w") as file:
                json.dump(
                    {
                        "seats": {
                            UPPER: 27,
                            LOWER: 27,
                            MIDDLE: 18,
                        }
                    },
                    file,
                    indent=4,
                )
            with open(file_path) as data:
                return json.load(data)
        else:
            with open(file_path) as data:
                return json.load(data)

    elif file == "train_seat_number":
        file_path = BASE_DIR / "data" / "train_seat_number.json"
        if not file_path.exists():
            with open(file_path, "w") as file:
                json.dump({'seat_number': {UPPER: [3, 6, 8, 11, 14, 16, 19, 22, 24, 27, 30, 32, 35, 38, 40, 43, 46, 48, 51, 54, 56, 59, 62, 64, 67, 70, 72],
                                    LOWER: [1, 4, 7, 9, 12, 15, 17, 20, 23, 25, 28, 31, 33, 36, 39, 41, 44, 47, 49, 52, 55, 57, 60, 63, 65, 68, 71], 
                                    MIDDLE: [2, 5, 10, 13, 18, 21, 26, 29, 34, 37, 42, 45, 50, 53, 58, 61, 66, 69]}}, file, indent=4)
            with open(file_path) as data:
                return json.load(data)
        else:
            with open(file_path) as data:
                return json.load(data)
    elif file == "booking_chart":
        file_path = BASE_DIR / "data" / "booking_chart.json"
        if not file_path.exists():
            with open(file_path, "w") as file:
                json.dump({"Fair collected": fair, "bookings": {}}, file, indent=4)
            with open(file_path) as data:
                return json.load(data)
        else:
            with open(file_path) as data:
                return json.load(data)
    else:
        raise ValueError(
            f"Invalid file name: {file}. Expected 'train_seats_count', 'train_seat_number' or 'booking_chart'."
        )


# Train class to handle seat bookings
class Train:
    def __init__(self):
        self._train_seats_data = get_json_data_path("train_seats_count")
        self.seats_data = load_json("train_seats_count")

    def save(self):
        with open(self._train_seats_data, "w") as file:
            json.dump(self.seats_data, file, indent=4)

    def book_lower(self):
        if self.seats_data["seats"][LOWER] > 0:
            self.seats_data["seats"][LOWER] -= 1
            self.save()
            print("Lower seat booked successfully!")
            return LOWER
        else:
            return self.book_middle()

    def book_middle(self):
        if self.seats_data["seats"][MIDDLE] > 0:
            self.seats_data["seats"][MIDDLE] -= 1
            self.save()
            print("Middle seat booked successfully!")
            return MIDDLE
        else:
            return self.book_upper()

    def book_upper(self):
        if self.seats_data["seats"][UPPER] > 0:
            self.seats_data["seats"][UPPER] -= 1
            self.save()
            print("Upper seat booked successfully!")
            return UPPER
        elif (
            self.seats_data["seats"][UPPER]
            + self.seats_data["seats"][MIDDLE]
            + self.seats_data["seats"][LOWER]
            == 0
        ):
            print("All seats are booked! No seats available.")
            return None
        else:
            if self.seats_data["seats"][MIDDLE] > 0:
                return self.book_middle()
            elif self.seats_data["seats"][LOWER] > 0:
                return self.book_lower()


# Main function to run the ticket booking system
def main():
    welcome_msg()
    book_or_cancel = get_input(
        prompt="Type 'Cancel' if you want to cancel a ticket or PRESS Enter to book a ticket: ",
        error_prompt="Not a valid input!",
    )
    if book_or_cancel.lower() == "cancel":
        print(cancel_ticket(get_input(prompt="Ticket_id: ", required=True)))
    elif book_or_cancel is (None or ""):
        username = get_verified_user()
        passenger_count = get_input(
            prompt="How many passengers would you like to book seats for? ",
            input_type="int",
            error_prompt="Not a valid passenger amount!",
        )
        print_map()
        select_station(passenger_count)
        book_ticket(username, passenger_count)
    else:
        print("Not a valid input!")


# Function to verify registered users
def get_verified_user():
    while True:
        username = get_input(prompt="Enter your PY-TICKET Username: ", required=True)
        if username not in registered_users:
            print("Not a registered user! ")
            continue
        return username


# Station selection and fair calculator
def select_station(passenger_count):
    global fair
    print("Your fair price is depends on the distance of your journey! \n1$ per 20 KM(Kilometer). ")
    try:
        input("If you want to continue with the booking press Enter or if you want to exit the program, press ctrl+C: ")
    except KeyboardInterrupt:
        exit("\nExited the booking app!")
    stations = {"pune": 0, "mumbai": 155, "jaipur": 1195, "delhi": 1407}
    station_list = list(stations.keys())
    while True:
        source = get_input(prompt=f"\nEnter SOURCE {station_list}: ", required=True).lower()
        if source not in station_list :
            print("Not found in the listed stations!")
            continue
        elif source == "delhi":
            print("Last station cannot be the SOURCE station (Train travels from Pune -> New Delhi)")
            continue
        station_index = station_list.index(source)
        while (station_index>=0):
            station_list.pop(station_index)
            station_index-=1
        break
    while True:
        destination = get_input(prompt=f"Enter DESTINATION {station_list}: ", required=True).lower()
        if destination not in station_list :
                print("Not found in the listed stations!")
                continue
        break
    fair += passenger_count*(stations.get(destination) - stations.get(source))/20
    print(f"\nYour Ticket price for {passenger_count} passengers is ${fair} (Cost per passenger: ${fair/passenger_count:.2f})")

# Get booking details from the user
def get_booking_details(i):
    print(f"\nENTER YOUR BOOKING DETAILS HERE FOR PASSENGER {i+1}:")
    name = get_input(prompt="Name: ", required=True)
    age = get_input(
        prompt="Age: ", required=True, input_type="int", error_prompt="Not a valid age!"
    )
    return (name, age)


# Algorithm to book seat type based on age filtering
def book_ticket(username, passenger_count):
    global fair
    train = Train()
    with open("ticket.txt", "w") as file:
        pass
    ticket_details = {"username":username, "name":[], "age":[], "seat_number":[], "seat_type":[], "id":[], "Ticket cost": fair}
    booking_chart = load_json("booking_chart")
    seat_number_array = load_json("train_seat_number")
    fair_collection = booking_chart["Fair collected"]
    booking_chart["Fair collected"] = fair_collection + fair    # Update the fair collection
    for i in range(passenger_count):
        name, age = get_booking_details(i)
        if age > 60:
            seat_type = train.book_lower()

        elif 30 <= age <= 60:
            seat_type = train.book_middle()
        else:
            seat_type = train.book_upper()

        seat_number = assign_seat_number(seat_type, seat_number_array)
        id = id_genrator(seat_type)

        if not (seat_type and seat_number and id):
            return None
        ticket_details["name"].append(name)
        ticket_details["age"].append(age)
        ticket_details["seat_number"].append(seat_number)
        ticket_details["seat_type"].append(seat_type)
        ticket_details["id"].append(id)

        booking_chart["bookings"].update({
            id: {
                "username": username,
                "name": name,
                "age": age,
                "seat_number": seat_number,
                "seat_type": seat_type,
                "ticket cost": fair/passenger_count
            }
            })             

    create_ticket(ticket_details, passenger_count)
    print("\nYour seats have all been booked, open ticket.txt to view your ticket!")
    
    # create a booking chart to display all passengers in the train (json file)
    with open(get_json_data_path("booking_chart"), "w") as file:
        json.dump(booking_chart, file, indent=4)

    # Update seat number in the json file
    with open(get_json_data_path("train_seat_number"), "w") as seat_number_file:
        json.dump(seat_number_array, seat_number_file, indent=4)



# Seat number data structure
def assign_seat_number(seat_type,seat_number_array):    
    if seat_type == None:
        return None
    try:
        if seat_type == LOWER:
            seat_number = seat_number_array["seat_number"][LOWER].pop(0)
        elif seat_type == MIDDLE:
            seat_number = seat_number_array["seat_number"][MIDDLE].pop(0)
        elif seat_type == UPPER:
            seat_number = seat_number_array["seat_number"][UPPER].pop(0)
        else:
          return None
    except IndexError:
        return None
    return seat_number


# ID Genrator
def id_genrator(seat_type):
    if seat_type != None:
        seat_code = seat_type[0]
    else:
        return None
    return f"{seat_code}-{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNPQRSTUVWXYZ')}{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNPQRSTUVWXYZ')}"


# Create ticket using ticket details of the passenger
def create_ticket(ticket_details, passenger_count):
    with open("ticket.txt", "a") as file:
        for i in range(len(ticket_details['id'])):
            file.write(
                f"Ticket under : {ticket_details['username']}\n Ticket Id: {ticket_details['id'][i]}\n Name: {ticket_details['name'][i]}\n Age: {ticket_details['age'][i]}\n Seat:{ticket_details['seat_number'][i]}\n {ticket_details['seat_type'][i]}\n Ticket cost: ${ticket_details['Ticket cost']/passenger_count}\n\n"
            )    
    

# Ticket cancellation based on unique ticket id
def cancel_ticket(cancel_id):
    chart_data = load_json("booking_chart")
    seat_count = load_json("train_seats_count")
    seat_number = load_json("train_seat_number")
    fair_collection = chart_data["Fair collected"]
    if cancel_id not in chart_data["bookings"]:
        return f"Invalid ID:{cancel_id}! Failed to cancel the ticket"
    cancelled_seat_type = chart_data["bookings"][cancel_id]["seat_type"]
    cancelled_seat_number = chart_data["bookings"][cancel_id]["seat_number"]
    refund_amount = chart_data["bookings"][cancel_id]["ticket cost"]
    seat_count["seats"][cancelled_seat_type] += 1
    seat_number["seat_number"][cancelled_seat_type].insert(0, cancelled_seat_number)
    chart_data["Fair collected"] = fair_collection - refund_amount
    del chart_data["bookings"][cancel_id]
    with open(get_json_data_path("train_seats_count"), "w") as file:
        json.dump(seat_count, file, indent=4)
    with open(get_json_data_path("train_seat_number"),"w") as file:
        json.dump(seat_number, file, indent=4)
    with open(get_json_data_path("booking_chart"),"w") as file:
        json.dump(chart_data, file, indent=4)
    return f"Ticket with ID: {cancel_id} successfully cancelled! You have been fully refunded."


if __name__ == "__main__":
    main()

