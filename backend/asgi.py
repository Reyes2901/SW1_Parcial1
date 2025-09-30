import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Primero establece la configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Inicializa Django antes de importar cualquier routing que use modelos
django_asgi_app = get_asgi_application()

# Ahora sí importa routing de tus apps
import diagrams.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Usa la instancia ya creada
    "websocket": AuthMiddlewareStack(
        URLRouter(
            diagrams.routing.websocket_urlpatterns
        )
    ),
})
