from django.urls import path , include
from lmsapp.consumers import CourierTrackingConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
	path("ws/track_courier/<int:courier_id>", CourierTrackingConsumer.as_asgi()) ,
]