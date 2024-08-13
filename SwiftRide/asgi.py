import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator  
from .middleware import TokenAuthMiddleware
from notifications.routing import websocket_urlpatterns as notifications_ws_urlpatterns

websocket_urlpatterns = [
    *notifications_ws_urlpatterns,

]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SwiftRide.settings.local")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
