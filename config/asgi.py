import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from ws.router import ws_urlpatterns
from ws.middlewares import AuthJWTMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthJWTMiddleware(
        URLRouter(ws_urlpatterns)
    ) 
})
