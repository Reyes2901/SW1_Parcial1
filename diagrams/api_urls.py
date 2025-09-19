from django.urls import path
from .api_views import DiagramListCreateAPI, DiagramDetailAPI

urlpatterns = [
    path('', DiagramListCreateAPI.as_view(), name='diagram-list-create'),
    path('<int:pk>/', DiagramDetailAPI.as_view(), name='diagram-detail'),
]
