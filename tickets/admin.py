from django.contrib import admin
from .models import Train, Station, Trips, Seat, Ticket

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('train_number', 'train_type', 'capacity', 'station1', 'station2')
    search_fields = ('train_number', 'train_type', 'station1__station_name', 'station2__station_name')
    list_filter = ('train_type', 'station1', 'station2')

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'station_code', 'governorate')
    search_fields = ('station_name', 'station_code')
    list_filter = ('governorate',)

@admin.register(Trips)
class Trips(admin.ModelAdmin):
    list_display = ('train', 'from_station','to_station','arrival_time', 'departure_time')
    search_fields = ('train__train_number', 'from_station__station_name','to_station__station_name')
    list_filter = ('from_station','to_station', 'train')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'class_type', 'train', 'is_available')
    search_fields = ('seat_number', 'train__train_number')
    list_filter = ('class_type', 'is_available', 'train')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'train', 'user', 'seat', 'from_station', 'to_station', 'arrival_time', 'departure_time', 'price', 'status')
    search_fields = ('ticket_number', 'user__email', 'train__train_number', 'seat__seat_number')
    list_filter = ('status', 'train', 'from_station', 'to_station')


