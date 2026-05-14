import requests
import json

BASE_URL = "http://127.0.0.1:8001"

def test_endpoints():
    # 1. Register
    reg_data = {
        "username": "testuser_final",
        "email": "test_final@example.com",
        "password": "Password123",
        "password2": "Password123"
    }
    print("Testing Register...")
    r = requests.post(f"{BASE_URL}/account/register/", data=reg_data)
    print(f"Status: {r.status_code}, Response: {r.text[:100]}")

    # 2. Login
    login_data = {
        "email": "test_final@example.com",
        "password": "Password123"
    }
    print("\nTesting Login...")
    r = requests.post(f"{BASE_URL}/account/login/", data=login_data)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        token = r.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print("Login failed")
        return

    # 3. User Details
    print("\nTesting User Details...")
    r = requests.get(f"{BASE_URL}/account/user-details/", headers=headers)
    print(f"Status: {r.status_code}, Data: {r.json()}")

    # 4. Search Trips with Date
    print("\nTesting Search Trips with Date...")
    search_data = {
        "from_station_id": 3, # Cairo
        "to_station_id": 4,   # Alexandria
        "date": "2026-06-01"
    }
    r = requests.post(f"{BASE_URL}/tickets/search-trips/", data=search_data)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        trips = r.json()
        if trips:
            trip_id = trips[0]['id']
            print(f"Found Trip ID: {trip_id}")
        else:
            print("No trips found")
            return
    else:
        print(f"Search failed: {r.text}")
        return

    # 5. Trip Seats
    print(f"\nTesting Trip Seats for trip {trip_id}...")
    r = requests.get(f"{BASE_URL}/tickets/trips/{trip_id}/seats/", params={"date": "2026-06-01"})
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        seats = r.json()
        available_seats = seats.get('available_seats', [])
        if available_seats:
            seat_id = available_seats[0]['seat_number']
            print(f"Found available seat: {seat_id}")
        else:
            print("No available seats")
            return
    else:
        print(f"Seats lookup failed: {r.text}")
        return

    # 6. Book Ticket
    print("\nTesting Ticket Booking...")
    book_data = {
        "trip_id": trip_id,
        "seat_id": 1, 
        "reservation_date": "2026-06-01"
    }
    r = requests.post(f"{BASE_URL}/tickets/book-ticket/", data=book_data, headers=headers)
    print(f"Status: {r.status_code}")
    if r.status_code == 201:
        print("Ticket booked successfully!")
        ticket_data = r.json()['ticket']
        ticket_number = ticket_data['ticket_number']
        print(f"Ticket Number: {ticket_number}")
    else:
        print(f"Booking failed: {r.text}")
        return

    # 7. Cancel Ticket
    print(f"\nTesting Ticket Cancellation for {ticket_number}...")
    r = requests.post(f"{BASE_URL}/tickets/cancel-ticket/{ticket_number}/", headers=headers)
    print(f"Status: {r.status_code}, Response: {r.json()}")

    # 8. Check Seats again
    print("\nVerifying seat release after cancellation...")
    r = requests.get(f"{BASE_URL}/tickets/trips/{trip_id}/seats/", params={"date": "2026-06-01"})
    seats = r.json()
    available_seat_numbers = [s['seat_number'] for s in seats.get('available_seats', [])]
    if "1" in available_seat_numbers:
        print("Success: Seat 1 is available again.")
    else:
        print("Failure: Seat 1 is still booked.")

if __name__ == "__main__":
    test_endpoints()