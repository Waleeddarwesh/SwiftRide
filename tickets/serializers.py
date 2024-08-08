from rest_framework import serializers
from .models import Train, Station, Seat, Ticket, Trips
import qrcode
from django.conf import settings
import os
from django.db import transaction

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class TripsSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)
    from_station = StationSerializer(read_only=True)
    to_station = StationSerializer(read_only=True)

    class Meta:
        model = Trips
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['seat_number', 'class_type', 'is_available']

class TicketSerializer(serializers.ModelSerializer):
    train = TrainSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    seat = SeatSerializer(read_only=True)
    from_station = StationSerializer(read_only=True)
    to_station = StationSerializer(read_only=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code:
            return request.build_absolute_uri(obj.qr_code.url)
        return None

class TicketBookingSerializer(serializers.Serializer):
    trip_id = serializers.PrimaryKeyRelatedField(queryset=Trips.objects.all())
    seat_id = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.filter(is_available=True))

    def validate_seat_id(self, seat):
        if not seat.is_available:
            raise serializers.ValidationError("This seat is already booked.")
        return seat

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to book a ticket.")
        trip = validated_data['trip_id']
        seat = validated_data['seat_id']

        with transaction.atomic():
            # Re-check if seat is available
            seat = Seat.objects.select_for_update().get(id=seat.id)
            if not seat.is_available:
                raise serializers.ValidationError("This seat is already booked.")
            
            # Mark the seat as booked
            seat.is_available = False
            seat.save()

            # Determine the price based on the trip
            price = trip.price  

            # Create the ticket
            ticket = Ticket.objects.create(
                user=user,
                train=trip.train,
                seat=seat,
                from_station=trip.from_station,
                to_station=trip.to_station,
                departure_time=trip.departure_time,
                arrival_time=trip.arrival_time,
                price=price,  
                status='Booked',
            )

            # Generate and save QR code
            qr_code_path = self.generate_qr_code(ticket)
            ticket.qr_code = qr_code_path
            ticket.save()

        return ticket

    def generate_qr_code(self, ticket):
        qr_data = {
            'Ticket Number': ticket.ticket_number,
            'Train Number': ticket.train.train_number,
            'Seat Number': ticket.seat.seat_number,
            'From Station': ticket.from_station.station_name,
            'To Station': ticket.to_station.station_name,
            'Departure Time': ticket.departure_time.isoformat(),
            'Arrival Time': ticket.arrival_time.isoformat(),
            'Price': str(ticket.price),
            'Status': ticket.status,
        }
        qr_code_data = "\n".join(f"{key}: {value}" for key, value in qr_data.items())

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Save QR Code to file
        qr_code_filename = f"{ticket.ticket_number}_qr.png"
        qr_code_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', qr_code_filename)
        os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
        img.save(qr_code_path)

        # Return the path relative to MEDIA_ROOT
        return os.path.join('qr_codes', qr_code_filename)

class TicketSearchSerializer(serializers.Serializer):
    from_station_id = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    to_station_id = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    departure_time = serializers.TimeField()