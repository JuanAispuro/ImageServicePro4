"""
ASGI config for artworks project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.urls import re_path
from collection import consumers

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from . import urls

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "artworks.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter([re_path(r"ws/socket-server", consumers.MsgConsumer.as_asgi())])
        )
        # Just HTTP for now. (We can add other protocols later.)
    }
)
