import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from sk_python_proj import sk_python_project

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sk_python_proj.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            sk_python_project.routing.websocket_urlpatterns
        )
    ),
})