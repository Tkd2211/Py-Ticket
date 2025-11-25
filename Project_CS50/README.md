#### Video Demo:  <URL HERE>
## Description:
PY-TICKET is a command-line based railway ticket booking system inspired by the Indian Railway Catering and Tourism Corporation (IRCTC). The project simulates a simplified version of the real booking system, with an emphasis on *age-based* seat allocation, a model used in parts of the Indian railway reservation system.

Users interact with the program entirely through the CLI, providing booking information step-by-step. When seats are successfully assigned, the system generates a `ticket.txt` file containing all booking details. The project also persists seat availability, fare collection data, and ticket records using json files, enabling a continuous and persistant state of data and the program.

The project currently applies its train booking logic on a singular coach with **72 seats** divided into 3 seat type category (Lower: 27 seats, Middle: 27 seats, Upper: 18 seats) in a coach layout exactly similar to found in modern Indian trains. 
     
## How to Use:
### Installation:
Download the project or clone the repository 
```
# git commands
git clone <your-repo-url>
cd <your-project-folder>
```

This project has no dependencies as this project only uses Python's built-in modules .

---

### How to run the program
Run the main script using: 
``` 
python project.py
```
This would run the program and ask for relevent ticket booking details iteratively for each passenger you want to book a ticket for. The program will end when either:
- seats have been successfully booked for each passneger in which case it would generate a `ticket.txt` file where a copy of your ticket with all the details would be found.
- or all seats have been booked in which case it would display a similar message and exit out gracefully.

```
 python reset.py all 
```
or reset a single JSON file (not advised due to irregular state  behaviour)
```
python reset.py train_seats_count

python reset.py train_seat_number

python reset.py booking_chart
```   

## Project  components:
#### 1. `Project.py`
 `project.py` serves as the main entry point for the CLI-based ticket booking system. It begins by validating the user through `get_verified_user()`, displays introductory ASCII art, and then guides the user through the booking or cancellation workflow. The program allows the user to select a source and destination from predefined stations, calculates the fare dynamically based on travel distance, and provides the option to cancel an existing ticket, restoring the released seat to the availability pool.

 During the booking process, the script collects passenger information, applies the age-based seat allocation algorithm, and generates a unique ticket ID. Once the booking is complete, the program writes all ticket details to ticket.txt and updates the system’s persistent JSON records.

 The script also coordinates updates to the core JSON data files: `train_seats_count.json` for seat availability, `train_seat_number.json` for remaining seat numbers, and `booking_chart.json` for tracking all issued tickets and total fare collection.

#### 2. `my_utilities/my_functions.py` :
 This module contains common utility functions used across the project. Many parts of the system require collecting and validating user input, often with constraints such as enforcing a specific data type (e.g., `str`, `int`) or ensuring non-empty input. The `get_input()` function centralizes this logic, allowing other modules to import and use it without repeating try/except blocks. This abstraction improves code readability, reduces duplication, and ensures consistent input validation throughout the application.

#### 3. `cli_art.py`:
 This is a local module used to output ASCII art required for the project.  
 It contains two predefined ASCII art functions — `welcome_msg()` and `print_map()` — which print the welcome message **"WELCOME TO PY-TICKET"** and the **route map**, respectively, in the terminal.

#### 4. `class Train`:
This class present inside `project.py` handles all updates related to seat availability and seat booking. It loads `train_seats_count.json` and updates it whenever a seat is booked.

- `self.seats_data` stores the the amount of available seats loaded from the json. Seats are categorized as **Upper**, **Lower**, and **Middle** mimicking a typical Indian train coach layout.
- `book_lower()` method books lower seats, primarily for passengers aged 60+ (if available) by reducing the seat count by 1. If not available, it calls other seat-type booking methods.
- `book_middle()` method books middle seats for passengers aged 31 to 60 (if available) by reducing the seat count by 1. If not available, it calls other seat-type booking methods.
- `book_upper()` method books upper seats (if available) by reducing the seat count by 1 . If not available, it calls other seat-type booking methods.


## Features :
- #### User Verification:
    As of now the user verification is a simple list lookup of the input string provided by the user. This feature needs to be expanded on in the future.

- #### Seat allocation algorithm:
    The seat allocation logic is based on simple age based algorithm.
    Users are divided into three age based categories (0 -> 30) (31 -> 60) (61 onwards). The eldest group (61 and onwards) gets the priority for the lower seat while the middle aged group (31 -> 60) gets priority over middle seat. The youngest group gets the upper seat. In case of a particular seat type being unavailable, each age group goes one level down in the seat priority heirarchy. Seat numbers are alloted serially (1 -> 72) so that each passenger group gets seats nearest to their group members.  

- #### Dynamic fare calculation:
    The fare system is distance-based and follows the rule of $1 per 20 km. Each station on the route (Pune → Mumbai → Jaipur → Delhi) has a predefined distance value, and the program computes the fare by subtracting the source distance from the destination distance. This calculation is multiplied by the number of passengers, producing a total fare for the booking session. The computed fare is also stored persistently in the JSON logs so that total revenue can be tracked across multiple runs of the program.

- #### Route Selection and Validation:
    The booking system ensures that users can only select valid source and destination stations from the defined route map. Users are prevented from choosing an impossible travel direction (e.g., selecting the final station as the source). The CLI enforces proper ordering of stations by dynamically pruning the list of remaining stations once a source is selected, improving usability and preventing logical errors during booking.

- #### Persistent Data Storage:
    The program maintains state across sessions using a set of JSON files. These track:
    - Available seats of each type
    - Unassigned seat numbers
    - Booking history and total fare collection
    This design allows the system to behave like a real reservation platform: seats remain booked even if the program is closed, and cancellations properly restore seat numbers and seat availability. JSON files were chosen for their readability, simple structure and primarily the ease of use.

- #### Ticket Cancellation System:
    Users can cancel a ticket using its unique ticket ID. Upon  cancellation, the system:
    - Restores the seat type count
    - Reinserts the seat number back into the seat pool
    - Refunds the appropriate fare amount
    - Removes the booking from the booking_chart.json
    This functionality ensures that cancellations behave consistently and that the booking data states remain accurate.

- #### Unique Ticket ID Generation:

    Each ticket is assigned a unique ID in the format 'X-####', where the first character X identifies the seat type (L/M/U). The remaining characters are randomly generated alphanumeric symbols, providing up to 62,500 possible combinations per seat type. This reduces the chance of collision and helps maintain a clean,    searchable booking history.

## Design chocies and lessons learned:
The biggest saving grace for this project was the integration of `get_input()` function. The **'my_utilities'** module was created by me (Github user: Tkd2211) during early weeks of following along CS50P. During the start of the final project this module was imported to the `~/project` folder to help with the CLI input handling in the project.
The `get_input()` was expaded on throughout the project to support more types data verification and handling. It also ended up saving us from major refactoring at the end of the project when we realised that we missed negative integer filtering while asking for stuff like passenger count and age. Fixing this bug turned to be as easy as refactoring the integer input logic of and adding an extra parameter to `get_input()`. This taught us the value of appropriate abstractions and pros of code modularity.

Another great insight came while testing the program for multiple file with multiple inputs while the program is in its iterative loop. While reading and writing the json files in data folder, the program felt slow. The reason behind this was quickly made out to be the inefficient use of `open()`. The `open()` was being called multiple times along with the `get_input()` function to read and write immdiately after taking the input. There were multiple disk I/O operations being executed in a single part of the program due to which it felt slowed down. This was solved by simply collecting all the input data in a dictionary and dumping it just once when all the data input and processing is finished.
This significantly improved the performance of the program and even improved the readability of the code.

## Future Scope of the project 
#### 1. Registration and Authetication
Currently the program is using a - list lookup on a predefined array 
- Use a password-based login
- Allow new registartions

#### 2. Host it as a Web App
- Host it as a web app with a front end and back end to integrate concureency features.

#### 3. Better Seat Allocation Algorithm
- Could use a scoring system for seat allocation priorities
- Berth preference selection (Lower/Middle/Upper)
- Special needs seating (pregnant women, disabled passengers)

#### 4. Add Functionalities and/or increase Scope of project 
- Multiple train models
- Concurrency support
- Mock payment gateway

