from channels.generic.websocket import AsyncJsonWebsocketConsumer


class UserNotifyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def send_message_to_user(self, event):
        await self.send_json(event)
