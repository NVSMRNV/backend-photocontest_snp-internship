from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotifyService:
    @staticmethod
    def send(user_id: int, message: dict) -> None:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{user_id}',
            {
                'type': 'send_notification',
                'message': message,
            },
        )
