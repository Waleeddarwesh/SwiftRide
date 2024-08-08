from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import *
import stripe
from django.conf import settings
     
class TicketSearchView(generics.GenericAPIView):
    serializer_class = TicketSearchSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        from_station = serializer.validated_data['from_station_id']
        to_station = serializer.validated_data['to_station_id']
        departure_time = serializer.validated_data['departure_time']

        # Query for available trips
        available_trips = Trips.objects.filter(
            from_station=from_station,
            to_station=to_station,
            departure_time=departure_time,
        )

        if not available_trips.exists():
            return Response({"detail": "No trips available for the selected criteria."}, status=404)

        # Assuming you have a serializer for Trips
        trip_serializer = TripsSerializer(available_trips, many=True)
        return Response(trip_serializer.data)
    
class TripSeatsView(generics.GenericAPIView):
    serializer_class = serializers.Serializer

    def get(self, request, *args, **kwargs):
        trip_id = kwargs.get('trip_id')
        try:
            trip = Trips.objects.get(id=trip_id)
        except Trips.DoesNotExist:
            return Response({"detail": "Trip not found."}, status=404)

        seats = Seat.objects.filter(train=trip.train)
        
        available_seats = seats.filter(is_available=True)
        booked_seats = seats.filter(is_available=False)

        available_seats_data = SeatSerializer(available_seats, many=True).data
        booked_seats_data = SeatSerializer(booked_seats, many=True).data

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
        
        return Response({
            'status': 'success',
            'ticket': TicketSerializer(ticket, context={'request': request}).data,
            'qr_code_url': qr_code_url
        }, status=status.HTTP_201_CREATED)