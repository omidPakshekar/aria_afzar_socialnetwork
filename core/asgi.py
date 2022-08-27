from __future__ import absolute_import, unicode_literals

import os
import chat.routing

from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ['DJANGO_CONFIGURATION'] = 'Dev'

from configurations.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": SessionMiddlewareStack(
        AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    chat.routing.websocket_urlpatterns
                )   
            )
        )
    )
})


