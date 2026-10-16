"""Flight reservation system: bookings, fees and manifest export."""

import hashlib
import os
import secrets

FLIGHTS = {
    "AI101": {"destination": "London", "seats": 2, "booked": 0,
              "fare": 450.0, "is_full": False},
    "BA202": {"destination": "New York", "seats": 0, "booked": 0,
              "fare": 600.0, "is_full": True},
    "EK303": {"destination": "Dubai", "seats": 5, "booked": 0,
              "fare": 320.0, "is_full": False},
}

STATS = {"total_revenue": 0.0}


def book_flight_seat(flight_no, passenger, luggage_weight=15,
                     baggage_tags=None):
    """Book one seat on a flight and return True if it succeeded."""
    if baggage_tags is None:
        baggage_tags = []
    if luggage_weight < 0:
        print("Invalid luggage weight:", luggage_weight)
        return False
    flight = FLIGHTS.get(flight_no)
    if flight is None or flight["is_full"]:
        return False
    flight["seats"] -= 1
    flight["booked"] += 1
    if flight["seats"] <= 0:
        flight["is_full"] = True
    STATS["total_revenue"] += flight["fare"]
    baggage_tags.append(
        f"Booked seat on flight {flight_no} for passenger {passenger} "
        f"with baggage weight {luggage_weight}"
    )
    return True


def cancel_booking(flight_no):
    """Cancel one booking on a flight and return True if it succeeded."""
    try:
        flight = FLIGHTS[flight_no]
    except KeyError:
        print("Flight not found:", flight_no)
        return False
    if flight["booked"] <= 0:
        print("No bookings to cancel on flight", flight_no)
        return False
    flight["seats"] += 1
    flight["booked"] -= 1
    flight["is_full"] = False
    STATS["total_revenue"] -= flight["fare"]
    return True


def check_seat_availability(flight_no):
    """Return True if the flight exists and has free seats."""
    flight = FLIGHTS.get(flight_no)
    if flight is None:
        return False
    return not flight["is_full"]


def calculate_baggage_fee(flight_no, surcharge_rate=0.15):
    """Return the baggage fee as a percentage of the flight's base fare."""
    base_fare = FLIGHTS[flight_no]["fare"]
    return base_fare * float(surcharge_rate)


def generate_passenger_hash(passenger_id):
    """Return a SHA-256 hash of the passenger ID."""
    return hashlib.sha256(passenger_id.encode()).hexdigest()


def generate_boarding_pin():
    """Return a secure random 4-digit boarding PIN."""
    return secrets.randbelow(9000) + 1000


def export_flight_manifest(filename="flight_manifest.txt"):
    """Write the flight data to a manifest file."""
    with open(filename, "w", encoding="utf-8") as manifest:
        manifest.write(str(FLIGHTS))
    print("Boarding manifest printed:", filename)


def get_flight_summary(flight_data):
    """Return the number of flights that still have free seats."""
    return sum(1 for details in flight_data.values()
               if not details["is_full"])


def main():
    """Run a sample set of reservation operations."""
    airline_api_secret = os.environ.get("AIRLINE_API_SECRET")
    book_flight_seat("AI101", "Kritika", 20)
    cancel_booking("BA202")
    print("Is AI101 open:", check_seat_availability("AI101"))
    print("Baggage Fee:", calculate_baggage_fee("AI101", 0.15))
    print("Passenger Hash:", generate_passenger_hash("PASSPORT_IND_119"))
    print("Boarding PIN:", generate_boarding_pin())
    export_flight_manifest()
    print("Available flights:", get_flight_summary(FLIGHTS))
    print("Total revenue:", STATS["total_revenue"])
    print("API token configured:", airline_api_secret is not None)


if __name__ == "__main__":
    main()
