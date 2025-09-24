from django.urls import path
from .api_views import DiagramListCreateAPI, DiagramDetailAPI, DiagramContentUpdateAPI, DiagramContentReadAPI

urlpatterns = [
    path('', DiagramListCreateAPI.as_view(), name='diagram-list-create'),
    path('<int:pk>/', DiagramDetailAPI.as_view(), name='diagram-detail'),

    # Nuevos endpoints para contenido JSON
    path('<int:pk>/content/', DiagramContentUpdateAPI.as_view(), name='diagram-content-update'),
    path('<int:pk>/content/read/', DiagramContentReadAPI.as_view(), name='diagram-content-read'),
]
    # path('<int:pk>/content/read/', DiagramContentReadAPI.as_view(), name='diagram-content-read'),
    