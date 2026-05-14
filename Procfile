web: daphne -b 0.0.0.0 -p $PORT SwiftRide.asgi:application
worker: celery -A SwiftRide worker -l info
