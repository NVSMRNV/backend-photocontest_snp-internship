from django.urls import path

from ws.consumers.users import UserNotifyConsumer


ws_urlpatterns = [
    path('ws/users/notify/', UserNotifyConsumer.as_asgi()),
]