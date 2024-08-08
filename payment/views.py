from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from tickets.models import Ticket
from .serializers import TicketInformationSerializer
from . import webhook

stripe.api_key = settings.STRIPE_SECRET_KEY

class TicketPaymentViewSet(viewsets.ViewSet):
    def get_serializer_class(self):
        if self.action == "process_payment":
            return TicketInformationSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["post"])
    def process_payment(self, request):
        serializer = TicketInformationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket_id = serializer.validated_data["ticket_id"]
        ticket = get_object_or_404(Ticket, ticket_number=ticket_id)

        success_url = request.build_absolute_uri(reverse("payment:success"))
        cancel_url = request.build_absolute_uri(reverse("payment:cancel"))

        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "client_reference_id": ticket.ticket_number,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [{
                "price_data": {
                    "unit_amount": int(ticket.price * Decimal("100")),
                    "currency": "EGP",
                    "product_data": {
                        "name": f"Ticket #{ticket.ticket_number}",
                    },
                },
                "quantity": 1,
            }],
        }

        session = stripe.checkout.Session.create(**session_data)
        return Response({"status": "success", "url": session.url})

@api_view(['GET'])
def payment_completed(request):
    webhook.stripe_webhook(request)
    return Response("Payment succeeded", status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def payment_canceled(request):
    return Response("Payment canceled ", status=status.HTTP_406_NOT_ACCEPTABLE)
