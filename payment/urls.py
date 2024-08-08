from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import payment_completed,payment_canceled,TicketPaymentViewSet
from . import webhook

app_name = "payment"

router = DefaultRouter()
router.register('ticket-payment', TicketPaymentViewSet, basename='ticket-payment')

urlpatterns = [
    path('success/',payment_completed , name='success'),
    path('canceled/', payment_canceled, name='cancel'),
    path('webhook/', webhook.stripe_webhook, name='stripe-webhook'),
    path('', include(router.urls)),
]