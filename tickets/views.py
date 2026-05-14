from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from notifications.tasks import send_notification_task

class TripsSearchView(generics.GenericAPIView):
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

        date = serializer.validated_data.get('date')
        
        final_trips = []
        for trip in available_trips:
            total_seats = Seat.objects.filter(train=trip.train).count()
            if date:
                reserved_count = SeatReservation.objects.filter(
                    trip=trip, 
                    reservation_date=date, 
                    reserved=True
                ).count()
                if reserved_count < total_seats:
                    final_trips.append(trip)
            else:
                # If no date provided, just show all trips (or default to today)
                final_trips.append(trip)

        if not final_trips:
            return Response({"detail": "No available trips found for the selected criteria and date."}, status=404)

        trip_serializer = TripsSerializer(final_trips, many=True)
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
        except (ValueError, AttributeError):
            from datetime import datetime
            try:
                reservation_date = datetime.strptime(date, '%Y-%m-%d').date()
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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        
        # Generate QR Code
        qr_code_url = serializer.generate_qr_code(ticket)
        request.session["ticket_id"] = str(ticket.ticket_number)
        # Send notification asynchronously
        message = f"hi {ticket.user.username}, Your Ticket {ticket.ticket_number} has been Booked."
        send_notification_task.delay(request.user.id, message)
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

class UserTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        status_filter = self.request.query_params.get('status')
        queryset = Ticket.objects.filter(user=self.request.user).order_by('-booking_date')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

class TicketCancellationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, ticket_number):
        try:
            ticket = Ticket.objects.get(ticket_number=ticket_number, user=request.user)
            if ticket.status == 'Cancelled':
                return Response({"detail": "Ticket already cancelled."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Release the seat reservation
            SeatReservation.objects.filter(
                trip__train=ticket.train, 
                seat=ticket.seat, 
                reservation_date=ticket.trip_date
            ).update(reserved=False)

            ticket.status = 'Cancelled'
            ticket.save()

            # Notify user
            send_notification_task.delay(request.user.id, f"Your ticket {ticket_number} has been cancelled.")

            return Response({"detail": "Ticket cancelled successfully."}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
    
