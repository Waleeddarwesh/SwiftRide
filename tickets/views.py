from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class TipsSearchView(generics.GenericAPIView):
    serializer_class = TripsSearchSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        from_station = serializer.validated_data['from_station_id']
        to_station = serializer.validated_data['to_station_id']

        available_trips = Trips.objects.filter(
            from_station=from_station,
            to_station=to_station,
        )

        if not available_trips.exists():
            return Response({"detail": "No trips available for the selected criteria."}, status=404)

        # Assuming you have a serializer for Trips
        trip_serializer = TripsSerializer(available_trips, many=True)
        return Response(trip_serializer.data)
    
class TripSeatsView(generics.GenericAPIView):
    serializer_class = SeatSerializer

    def get(self, request, *args, **kwargs):
        trip_id = kwargs.get('trip_id')
        date = request.query_params.get('date')  

        if not date:
            return Response({"detail": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            trip = Trips.objects.get(id=trip_id)
        except Trips.DoesNotExist:
            return Response({"detail": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            reservation_date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get all seats for the trip
        seats = Seat.objects.filter(train=trip.train)
        
        # Find reserved seats for the specified date
        reserved_seats = SeatReservation.objects.filter(trip=trip, reservation_date=reservation_date, reserved=True)
        reserved_seat_ids = reserved_seats.values_list('seat_id', flat=True)
        
        # Split seats into available and booked based on reservations
        available_seats = seats.exclude(id__in=reserved_seat_ids)
        booked_seats = seats.filter(id__in=reserved_seat_ids)

        # Pass context with reservation_date
        available_seats_data = SeatSerializer(available_seats, many=True, context={'trip_id': trip_id, 'reservation_date': reservation_date}).data
        booked_seats_data = SeatSerializer(booked_seats, many=True, context={'trip_id': trip_id, 'reservation_date': reservation_date}).data

        return Response({
            "available_seats": available_seats_data,
            "booked_seats": booked_seats_data
        })
    
class TicketBookingView(generics.GenericAPIView):
    serializer_class = TicketBookingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        
        # Generate QR Code
        qr_code_url = serializer.generate_qr_code(ticket)
        request.session["ticket_id"] = str(ticket.ticket_number)
        # Send notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{request.user.id}",
            {
            "type": "send_notification",
            "message": f" hi {ticket.user.username},Your Ticket {ticket.ticket_number} has been Booked."
             }
             )
        return Response({
            'status': 'success',
            'ticket': TicketSerializer(ticket, context={'request': request}).data,
            'qr_code_url': qr_code_url
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_train_location(request, train_number):
    try:
        train = Train.objects.get(train_number=train_number)
        data = {
            "latitude": train.current_latitude,
            "longitude": train.current_longitude,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Train.DoesNotExist:
        return Response({"error": "Train not found"}, status=status.HTTP_404_NOT_FOUND)
       
@api_view(['POST'])
def update_train_location(request, train_number):
    try:
        train = Train.objects.get(train_number=train_number)
        train.current_latitude = request.data.get('latitude')
        train.current_longitude = request.data.get('longitude')
        train.save()
        return Response({"status": "location updated"}, status=status.HTTP_200_OK)
    except Train.DoesNotExist:
        return Response({"error": "Train not found"}, status=status.HTTP_404_NOT_FOUND)
    
