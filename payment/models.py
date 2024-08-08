from django.db import models
from account.models import User
from tickets.models import Ticket
# Create your models here.

class PaymentHistory(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Ticket=models.ForeignKey(Ticket, on_delete=models.SET_NULL, blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    payment_status=models.BooleanField()

    def __str__(self):
        return self.Ticket.ticket_number