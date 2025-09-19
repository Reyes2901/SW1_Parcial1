from django.urls import path, include

urlpatterns = [
    # Incluye aquí las rutas de tus apps, por ejemplo:
    # path('miapp/', include('miapp.urls')),
    path('diagrams/', include('diagrams.urls')),
    path('api/diagrams/', include('diagrams.api_urls')),
    path('generator/', include('generator.urls')),
]