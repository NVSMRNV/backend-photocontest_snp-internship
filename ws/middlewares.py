from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.tokens import AccessToken

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from models.models.users.models import User


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get('token', [None])[0]

        scope['user'] = await self.get_user(token)
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            if token:
                access_token = AccessToken(token)
                return User.objects.get(id=access_token['user_id'])
        except Exception:
            return AnonymousUser()
