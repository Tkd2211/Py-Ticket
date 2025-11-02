"""
Yes — your TBOOKER idea fits those CS50P final project requirements perfectly, with only small adjustments to structure and scope.
Let’s check everything point-by-point to make sure you’re 100% compliant 👇

📁 Project structure (CS50P-compatible)
tbooker/
│
├── project.py          # ✅ main() + 3+ top-level functions
├── test_project.py     # ✅ pytest tests for the functions in project.py
├── requirements.txt    # ✅ list any libraries (e.g., pyfiglet)
│
├── train.py            # optional — Train class
├── user.py             # optional — User class
├── data/
│   ├── users.json
│   ├── trains.json
│   └── bookings.json
└── my_utilities/
    └── my_functions.py


📜 Let’s map your project to the CS50P requirements
CS50P RequirementDoes TBOOKER meet it?HowImplemented in Python✅Entirely CLI-based PythonHas main()✅Your entry point for the CLI menu (in project.py)3 or more additional functions✅You can easily include: • get_verified_user()• book_ticket()• view_bookings() (or save_booking())Each function at same indentation as main() (not inside a class)✅Keep those core functions top-level; classes (like Train) can still be imported and used inside themAt least 3 testable functions with pytest✅You can test: • get_verified_user() (with mocked input)• book_ticket() (with sample data)• calculate_remaining_seats() (pure function for easy testing)test_project.py with pytest functions✅Define test_get_verified_user(), test_book_ticket(), etc.More time and effort than a problem set✅This includes OOP, file handling, testing, and CLI logicList dependencies in requirements.txt✅e.g.:pyfigletcolorama (optional)

💡 Example: Core project.py outline
import json
import pyfiglet
from train import Train

def main():
    f = pyfiglet.Figlet(font="block")
    print(f.renderText("WELCOME TO TBOOKER"))
    username = get_verified_user()
    book_ticket(username)

def get_verified_user():
    username = input("Enter username: ")
    users = load_users()
    if username not in users:
        print("User not registered.")
        return None
    return username

def book_ticket(username):
    train = Train()
    seat_type = input("Enter seat type (lower/middle/upper): ").lower()
    success = train.book_seat(seat_type)
    if success:
        save_booking(username, seat_type)
        print(f"{seat_type.title()} seat booked for {username}!")
    else:
        print("No seats available.")

def save_booking(username, seat_type):
    booking = {"username": username, "seat_type": seat_type}
    with open("data/bookings.json", "a") as f:
        json.dump(booking, f)
        f.write("\n")

# Helper
def load_users():
    with open("data/users.json") as f:
        return json.load(f)

if __name__ == "__main__":
    main()


🧪 Example test_project.py
import pytest
from project import get_verified_user, save_booking

def test_save_booking(tmp_path):
    file = tmp_path / "bookings.json"
    from project import save_booking
    save_booking("Tejas_4", "lower")
    # check if file has correct JSON line
    with open("data/bookings.json") as f:
        line = f.readline()
        assert '"Tejas_4"' in line

def test_load_users(tmp_path):
    file = tmp_path / "users.json"
    file.write_text('["Tejas_4", "Yash_5"]')
    from project import load_users
    users = load_users()
    assert "Tejas_4" in users

def test_book_ticket(monkeypatch):
    from train import Train
    train = Train()
    monkeypatch.setattr("builtins.input", lambda _: "lower")
    result = train.book_seat("lower")
    assert result == True


📦 requirements.txt example
pyfiglet
pytest
colorama


✅ In summary
Your TBOOKER idea:


✅ Fully Python-based


✅ Uses OOP and file I/O


✅ Has testable functions


✅ Has a clear main()


✅ Fits CS50P expectations for effort and structure


So you don’t need to scrap it — just keep it console-only, store data in JSON, and make sure your 3+ core functions live in project.py (so they’re easy to test).

Would you like me to suggest exactly which three functions would be easiest and most meaningful to test with pytest for your final submission?

"""