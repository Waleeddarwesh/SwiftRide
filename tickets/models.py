from django.db import models
from account.models import User
import uuid

# Create your models here.
class Train(models.Model):
    TRAIN_TYPES = [
        ('Express', 'Express'),
        ('Regional', 'Regional'),
        ('Freight', 'Freight'),
    ]

    train_number = models.CharField(max_length=50, unique=True)
    train_type = models.CharField(max_length=50, choices=TRAIN_TYPES)
    capacity = models.PositiveIntegerField()
    station1 = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, related_name='station1')
    station2 = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, related_name='station2')

    def __str__(self):
        return f"{self.train_number} ({self.train_type})"

class Station(models.Model):
    station_name = models.CharField(max_length=100)
    station_code = models.CharField(max_length=10, unique=True)
    governorate = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.station_name} ({self.station_code})"

class Trips(models.Model):
    from_station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, related_name='from_station')
    to_station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, related_name='to_station')
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

    def __str__(self):
        return f"{self.train.train_number} from {self.from_station.station_name} to {self.to_station.station_name}"

class Seat(models.Model):
    CLASS_TYPES = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('First', 'First Class'),
    ]

    seat_number = models.CharField(max_length=10)
    class_type = models.CharField(max_length=50, choices=CLASS_TYPES)
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='seats')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Seat {self.seat_number} ({self.class_type}) in Train {self.train.train_number}"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('paid', 'paid'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    ticket_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True)
    from_station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, related_name='from_ticket_station')
    to_station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True, related_name='to_ticket_station')
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    booking_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_id = models.CharField(max_length=250,null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Booked')
    qr_code = models.ImageField(upload_to='ticket_qr_codes/', null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.ticket_number} for {self.user.email}"

