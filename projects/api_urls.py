from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProjectViewSet
from .collaborator_views import CollaboratorListCreateView, CollaboratorDeleteView

router = DefaultRouter()
# Registrar el ViewSet del proyecto
router.register(r'', ProjectViewSet, basename='project')#, basename='project')

urlpatterns = router.urls

urlpatterns += [
    path('<int:project_id>/collaborators/', CollaboratorListCreateView.as_view(), name='collaborator-list-create'),
    path('<int:project_id>/collaborators/<int:user_id>/', CollaboratorDeleteView.as_view(), name='collaborator-delete'),
]

# --- IGNORE ---