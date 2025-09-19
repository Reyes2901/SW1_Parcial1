from django.urls import path
from .views import generar_backend_zip

urlpatterns = [
    path('<int:diagram_id>/generate/', generar_backend_zip, name='generate-backend'),
]
