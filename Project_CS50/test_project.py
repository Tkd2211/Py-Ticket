import json
from project import (
    get_json_data_path,
    load_json,
    Train,
    assign_seat_number,
    id_genrator,
    cancel_ticket,
    LOWER, MIDDLE, UPPER
)


def test_get_json_data_path():
    path = get_json_data_path("train_seats_count")
    assert path.exists()
    assert "train_seats_count.json" in str(path)


def test_load_json_returns_dict():
    data = load_json("train_seats_count")
    assert isinstance(data, dict)
    assert "seats" in data


def test_book_lower():
    train =Train()
    old = train.seats_data["seats"][LOWER]
    if old == 0:
        old+=1
    train.book_lower()
    new = train.seats_data["seats"][LOWER]
    assert new == old - 1


def test_book_middle():
    train = Train()
    old = train.seats_data["seats"][MIDDLE]
    if old == 0:
        old+=1
    train.book_middle()
    new = train.seats_data["seats"][MIDDLE]
    assert new == old - 1


def test_book_upper():
    train = Train()
    old = train.seats_data["seats"][UPPER]
    if old == 0:
        old+=1
    train.book_upper()
    new = train.seats_data["seats"][UPPER]
    assert new == old - 1


def test_age_above_60_gets_lower():
    train = Train()
    train.seats_data["seats"][LOWER] = 5
    train.save()
    age = 65
    if age > 60:
        seat = train.book_lower()
    elif 30 <= age <= 60:
        seat = train.book_middle()
    else:
        seat = train.book_upper()

    assert seat == LOWER


def test_age_between_30_and_60_gets_middle():
    train =Train()
    train.seats_data["seats"][MIDDLE] = 5
    train.save()
    age = 45
    if age > 60:
        seat = train.book_lower()
    elif 30 <= age <= 60:
        seat = train.book_middle()
    else:
        seat = train.book_upper()
    assert seat == MIDDLE


def test_age_below_30_gets_upper():
    train = Train()
    train.seats_data["seats"][UPPER] = 5
    train.save()
    age = 20
    if age > 60:
        seat = train.book_lower()
    elif 30 <= age <= 60:
        seat = train.book_middle()
    else:
        seat = train.book_upper()
    assert seat == UPPER


def test_assign_seat_number():
    seat_data = {
        "seat_number": {
            LOWER: [1, 2],
            MIDDLE: [3, 4],
            UPPER: [5, 6]
        }
    }
    n = assign_seat_number(LOWER, seat_data)
    assert n == 1
    assert seat_data["seat_number"][LOWER] == [2]


def test_id_genrator():
    generated = id_genrator(LOWER)
    assert isinstance(generated, str)
    assert len(generated) == 6
    assert generated[0] == "L"

    generated = id_genrator(UPPER)
    assert isinstance(generated, str)
    assert len(generated) == 6
    assert generated[0] == "U"


def test_cancel_ticket_invalid():
    result = cancel_ticket("FAKE-ID-123")
    assert "Invalid ID" in result


def test_cancel_ticket_valid():
    chart_path = get_json_data_path("booking_chart")
    chart_data = load_json("booking_chart")
    chart_data["bookings"]["T-1A1A"] = {
        "username": "User_1",
        "name": "Test",
        "age": 40,
        "seat_number": 99,
        "seat_type": LOWER,
        "ticket cost": 10
    }

    chart_data["fare collected"] += 10
    with open(chart_path, "w") as file:
        json.dump(chart_data, file, indent=4)
    result = cancel_ticket("T-1A1A")
    assert "successfully cancelled" in result
    updated = load_json("booking_chart")
    assert "T-1A1A" not in updated["bookings"]


def test_booking_stops_when_empty():
    train =Train()
    train.seats_data["seats"][LOWER] = 0
    train.seats_data["seats"][MIDDLE] = 0
    train.seats_data["seats"][UPPER] = 0
    train.save()
    assert train.book_upper() is None


def test_empty_assign_seat_number():
    data = {"seat_number": {LOWER: []}}
    assert assign_seat_number(LOWER, data) is None


def test_json_updates_after_booking():
    train =Train()
    before = train.seats_data["seats"][LOWER]
    train.seats_data["seats"][LOWER] = before if before > 0 else 1
    train.save()
    train.book_lower()
    after = load_json("train_seats_count")["seats"][LOWER]
    assert after == train.seats_data["seats"][LOWER]


def test_id_generator_format():
    ticket_id = id_genrator(UPPER)
    assert isinstance(ticket_id, str)
    assert ticket_id[0] == "U"
    assert any(char.isdigit() for char in ticket_id)


def test_json_initialization():
    seats = load_json("train_seats_count")
    assert "seats" in seats
    assert LOWER in seats["seats"]
    assert MIDDLE in seats["seats"]
    assert UPPER in seats["seats"]


def test_train_save():
    train = Train()
    train.seats_data["seats"][LOWER] = 5
    train.save()
    data = load_json("train_seats_count")

    assert data["seats"][LOWER] == 5
