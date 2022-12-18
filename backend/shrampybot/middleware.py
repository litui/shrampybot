from django.contrib.auth.models import AnonymousUser, User
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from queue import Queue
from daphne.server import Server

@database_sync_to_async
def get_user(user_id):
    return User.objects.get(id=user_id)


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive: Queue.get, send: Server.handle_reply):
        token_parts = scope['subprotocols']
        try:
            token = AccessToken(token_parts[1])
            user_id = token.get('user_id', None)
        except (IndexError, TokenError):
            token = None
            user_id = None

        scope['user'] = AnonymousUser() if user_id is None else await get_user(user_id)
        return await super().__call__(scope, receive, send)