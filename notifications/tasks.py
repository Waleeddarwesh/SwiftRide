from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

@shared_task
def send_notification_task(user_id, message):
    # Save to database
    Notification.objects.create(user_id=user_id, message=message)
    
    # Send to websocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "message": message
        }
    )
    return f"Notification sent to user {user_id}"
