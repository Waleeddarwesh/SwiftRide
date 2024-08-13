from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import HttpResponse, render
from .models import Notification
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer
from account.models import User

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
def send_notification_to_users(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message:
            users = User.objects.all()
            channel_layer = get_channel_layer()
            for user in users:
                # Save notification to the database
                Notification.objects.create(user=user, message=message)

                # Send notification over the WebSocket
                group_name = f"user_{user.id}"
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {
                        'type': 'send_notification',
                        'message': message,
                    }
                )
        return HttpResponse("Notifications sent to all users.")
