import pyfiglet
from my_utilities.my_functions import get_input

registered_users = ["Tejas_4", "Yash_5"]


class Train:
    def __init__(self):
        self.lower_seats = 27  # Total amount of lower seats in a single coach
        self.upper_seats = 27  # Total amount of upper seats in a single coach
        self.middle_seats = 18  # Total amount of middle seats in a single coach

    def book_lower(self):
        if self.lower_seats > 0:
            self.lower_seats -= 1
        else:
            return "Full"
        print("Lower seat booked successfully!")

    def book_upper(self):
        if self.upper_seats > 0:
            self.upper_seats -= 1
        else:
            return "Full"
        print("Upper seat booked successfully!")

    def book_middle(self):
        if self.middle_seats > 0:
            self.middle_seats -= 1
        else:
            return "Full"
        print("Middle seat booked successfully!")


def main():
    f = pyfiglet.Figlet(font="slant")  # needs better font(?)
    print(f.renderText("WELCOME TO TBOOKER"))
    username = get_verified_user()
    age = get_booking_details()
    seat_type = book_ticket(age)
    create_ticket(username, age, seat_type)


def get_verified_user():
    while True:
        username = get_input(prompt="Enter your TBOOKER Username: ", required=True)
        if username not in registered_users:
            print("Not a registered user! ")
            continue
        return username


def get_booking_details():  # LOT MORE BOOKING DETAILS TO ADD (MAYBE?)
    print("ENTER YOUR BOOKING DETAILS HERE!")
    while True:
        try:
            age = int(get_input(prompt="Age: ", required=True))
        except ValueError:
            print("Not a Valid age! Try again.")
            continue
        return age


def book_ticket(a):  # ADD ALGORITHM TO BOOK SEAT TYPE BASED ON AGE FILTERING
    train = Train()
    train.book_lower()
    return "(to-be-added)-seat"


def create_ticket(username, age, seat_type):  # BETTER FORMAT FOR PRINTING A TICKET
    with open("ticket.txt", "w") as file:
        file.write(
            f"Ticket under : {username}\n" + f"Age: {age}\n" + f"Seat: {seat_type}"
        )


if __name__ == "__main__":
    main()
