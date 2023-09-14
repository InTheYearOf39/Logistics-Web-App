import json
from channels.generic.websocket import AsyncWebsocketConsumer
from lmsapp.models import User 

class CourierTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.courier_id = self.scope['url_route']['kwargs']['courier_id']
        self.room_group_name = f"courier_{self.courier_id}"

        # Check if the courier exists in your database
        try:
            self.courier = User.objects.get(id=self.courier_id)
        except User.DoesNotExist:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group when the WebSocket is closed.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def track_courier(self, event):
        # Send courier tracking data to the WebSocket
        await self.send(text_data=json.dumps(event))
