from rest_framework import serializers
from .models import Train, Station, Seat, Ticket, Trips,SeatReservation
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
    is_reserved = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['seat_number', 'class_type', 'is_reserved']

    def get_is_reserved(self, seat):
        trip_id = self.context.get('trip_id')
        reservation_date = self.context.get('reservation_date')

        if trip_id and reservation_date:
            return SeatReservation.objects.filter(seat=seat, trip_id=trip_id, reserved=True, reservation_date=reservation_date).exists()
        return False

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
    seat_id = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())
    reservation_date = serializers.DateField()

    def validate(self, data):
        trip = data['trip_id']
        seat = data['seat_id']
        reservation_date = data['reservation_date']

        
        if SeatReservation.objects.filter(seat=seat, trip=trip, reserved=True, reservation_date=reservation_date).exists():
            raise serializers.ValidationError("This seat is already reserved for the selected trip on the specified date.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to book a ticket.")
        
        trip = validated_data['trip_id']
        seat = validated_data['seat_id']
        reservation_date = validated_data['reservation_date']

        with transaction.atomic():
            if SeatReservation.objects.filter(seat=seat, trip=trip, reserved=True, reservation_date=reservation_date).exists():
                raise serializers.ValidationError("This seat is already reserved for the selected trip on the specified date.")
            
            # Reserve the seat for the trip and date
            SeatReservation.objects.create(
                trip=trip,
                seat=seat,
                reservation_number=SeatReservation.objects.filter(trip=trip, seat=seat, reservation_date=reservation_date).count() + 1,
                reserved=True,
                reservation_date=reservation_date
            )

            # Create the ticket
            ticket = Ticket.objects.create(
                user=user,
                train=trip.train,
                seat=seat,
                from_station=trip.from_station,
                to_station=trip.to_station,
                departure_time=trip.departure_time,
                arrival_time=trip.arrival_time,
                trip_date = reservation_date,
                price=trip.price,
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

class TripsSearchSerializer(serializers.Serializer):
    from_station_id = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    to_station_id = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    