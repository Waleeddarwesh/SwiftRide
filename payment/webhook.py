import stripe
from django.conf import settings
from decimal import Decimal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from tickets.models import Ticket, SeatReservation
from .models import PaymentHistory
from notifications.tasks import send_notification_task

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == "checkout.session.completed":
        session = event['data']['object']

        if session['mode'] == "payment" and session['payment_status'] == "paid":
            client_reference_id = session['client_reference_id']
            ticket_id = client_reference_id  

            try:
                ticket = Ticket.objects.get(ticket_number=ticket_id)
                # Update ticket status
                ticket.status = 'paid'
                ticket.stripe_id = session['payment_intent']  
                ticket.save()
                
                # Record Payment History
                PaymentHistory.objects.create(
                    user=ticket.user,
                    Ticket=ticket,
                    payment_status=True
                )

                # Update Supplier Balance
                if ticket.train.supplier:
                    supplier = ticket.train.supplier
                    price = float(ticket.price)
                    supplier.balance += Decimal(str(price * 0.85)) # 15% commission
                    supplier.save()
                
                # Send confirmation notification
                message = f"Payment confirmed for Ticket {ticket.ticket_number}. Your trip is ready!"
                send_notification_task.delay(ticket.user.id, message)

                return HttpResponse(status=200)
            except Ticket.DoesNotExist:
                return HttpResponse(status=404)

    return HttpResponse(status=200)
