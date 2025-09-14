from django.urls import path
from .views import RegistroAPIView, LoginAPIView, PerfilAPIView, LogoutAPIView

urlpatterns = [
    path('registro/', RegistroAPIView.as_view(), name='registro'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('perfil/', PerfilAPIView.as_view(), name='perfil'),
]
