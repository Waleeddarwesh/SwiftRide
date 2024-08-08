from django.urls import path
from .views import *

urlpatterns=[
    path('search-tickets/', TicketSearchView.as_view(), name='search-tickets'),
    path('trips/<int:trip_id>/seats/', TripSeatsView.as_view(), name='trip-seats'),
    path('book-ticket/', TicketBookingView.as_view(), name='book-ticket'),
]