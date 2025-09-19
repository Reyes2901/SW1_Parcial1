from django.urls import path
from . import views

app_name = 'diagrams'

urlpatterns = [
    path('project/<int:project_id>/diagrams/', views.diagram_list, name='diagram_list'),
    path('diagram/<int:pk>/', views.diagram_detail, name='diagram_detail'),
    path('project/<int:project_id>/create/', views.diagram_create, name='diagram_create'),
    path('diagram/<int:pk>/edit/', views.diagram_edit, name='diagram_edit'),
    path('diagram/<int:pk>/delete/', views.diagram_delete, name='diagram_delete'),
]
