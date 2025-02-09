# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  
from config.asgi_adapter import ASGI3toASGI2Adapter 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django_asgi_app = get_asgi_application()
django_asgi_app = ASGI3toASGI2Adapter(django_asgi_app)

application = ProtocolTypeRouter({
    #"http": get_asgi_application(),
    "http": django_asgi_app,  
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
