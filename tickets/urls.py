from django.urls import path
from .views import *

urlpatterns=[
    path('search-trips/', TripsSearchView.as_view(), name='search-tickets'),
    path('trips/<int:trip_id>/seats/', TripSeatsView.as_view(), name='trip-seats'),
    path('book-ticket/', TicketBookingView.as_view(), name='book-ticket'),
    path('update-location/<str:train_number>/', update_train_location, name='update_train_location'),
    path('get-location/<str:train_number>/', get_train_location, name='get_train_location'),
    path('my-tickets/', UserTicketListView.as_view(), name='my-tickets'),
    path('cancel-ticket/<uuid:ticket_number>/', TicketCancellationView.as_view(), name='cancel-ticket'),
]
