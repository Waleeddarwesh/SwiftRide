import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SwiftRide.settings')
django.setup()

from account.models import User
from tickets.models import Train, Station, Trips, Seat

def seed_data():
    # Stations
    s1, _ = Station.objects.get_or_create(station_name="Cairo", station_code="CAI", governorate="Cairo")
    s2, _ = Station.objects.get_or_create(station_name="Alexandria", station_code="ALX", governorate="Alexandria")

    # Train
    t, _ = Train.objects.get_or_create(
        train_number="T101", 
        defaults={
            "train_type": "Express", 
            "capacity": 100,
            "station1": s1,
            "station2": s2
        }
    )

    # Seats
    for i in range(1, 11):
        Seat.objects.get_or_create(
            seat_number=str(i), 
            train=t, 
            defaults={"class_type": "Economy"}
        )

    # Trip
    Trips.objects.get_or_create(
        from_station=s1,
        to_station=s2,
        train=t,
        defaults={
            "arrival_time": "10:00:00",
            "departure_time": "08:00:00",
            "price": 50.00
        }
    )

    print("Seed data created successfully.")

if __name__ == "__main__":
    seed_data()
