import datetime
from rest_framework import serializers
from tickets.models import Ticket

def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")

def check_expiry_year(value):
    today = datetime.datetime.now()
    if not int(value) >= today.year:
        raise serializers.ValidationError("Invalid expiry year.")

def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid cvc number.")

def check_payment_method(value):
    payment_method = value.lower()
    if payment_method not in ["card"]:
        raise serializers.ValidationError("Invalid payment_method.")

class TicketInformationSerializer(serializers.Serializer):
    ticket_id = serializers.UUIDField()

    def validate_order_id(self, value):
        if not Ticket.objects.filter(id=value).exists():
            raise serializers.ValidationError("Ticket with the given ID does not exist.")
        return value
    
