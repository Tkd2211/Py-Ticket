import json
import sys
from project_CS50 import get_json_data_path

def main():
    file_name = get_argument()
    reset(file_name)

def get_argument():
    if len(sys.argv)==2:
        arg1 = sys.argv[1].lower()
        return arg1
    elif len(sys.argv)==1:
        sys.exit("Type file name (no need for .json extension). Use 'all' to reset all json files in data dir. ")
    else:
        sys.exit("Incorrect amount of arguments!")

def reset(file_name):
    reset_train_seats_count = get_json_data_path(file="train_seats_count")
    reset_train_seat_number = get_json_data_path(file="train_seat_number")
    match file_name:
        case "train_seats_count":
            with open(reset_train_seats_count,"w") as file:
                json.dump({"seats": {"upper_seats": 27, "lower_seats": 27, "middle_seats": 18 }}, file, indent=4)
        case "train_seat_number":
            with open(reset_train_seat_number,"w") as file:
                json.dump({'seat_number': {'upper_seat_number': [3, 6, 8, 11, 14, 16, 19, 22, 24, 27, 30, 32, 35, 38, 40, 43, 46, 51, 56, 59, 64, 67, 70, 72], 
                                    'lower_seat_number': [1, 4, 7, 9, 12, 15, 17, 20, 23, 25, 28, 31, 33, 36, 39, 41, 44, 47, 52, 55, 57, 60, 63, 65, 68, 71], 
                                    'middle_seat_number': [2, 5, 10, 13, 18, 21, 26, 29, 34, 37, 42, 45, 50, 53, 58, 61, 66, 69]}}, file, indent=4)
        case "all":
            with open(reset_train_seats_count,"w") as file:
                json.dump({"seats": {"upper_seats": 27, "lower_seats": 27, "middle_seats": 18 }}, file, indent=4)
            with open(reset_train_seat_number,"w") as file:
                json.dump({'seat_number': {'upper_seat_number': [3, 6, 8, 11, 14, 16, 19, 22, 24, 27, 30, 32, 35, 38, 40, 43, 46, 51, 56, 59, 64, 67, 70, 72],
                                    'lower_seat_number': [1, 4, 7, 9, 12, 15, 17, 20, 23, 25, 28, 31, 33, 36, 39, 41, 44, 47, 52, 55, 57, 60, 63, 65, 68, 71], 
                                    'middle_seat_number': [2, 5, 10, 13, 18, 21, 26, 29, 34, 37, 42, 45, 50, 53, 58, 61, 66, 69]}}, file, indent=4)
        case _:
            sys.exit("Not a valid file name")


if __name__=="__main__":
    main()
