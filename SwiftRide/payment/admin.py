from django.contrib import admin
from .models import PaymentHistory

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'Ticket', 'date', 'payment_status')
    search_fields = ('user__email', 'Ticket__ticket_number')
    list_filter = ('payment_status', 'date')
    ordering = ('-date',)