"""
ASGI config for shrampybot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from .middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shrampybot.settings')
django_asgi_app = get_asgi_application()

import service.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddleware(URLRouter(service.routing.websocket_urlpatterns))
        ),
})