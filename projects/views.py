from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from users import models
from .models import Project
from .forms import ProjectForm
from .permissions import can_edit_project, can_delete_project, IsProjectOwner
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from rest_framework import viewsets
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

from rest_framework.exceptions import NotFound
#cambio para que busque por PK
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"  #Asegura que solo busque por id

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(collaborators=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_object(self):
        obj = super().get_object()  # Esto ya buscará solo por id
        if self.request.user != obj.owner and self.request.user not in obj.collaborators.all():
            raise NotFound("Proyecto no encontrado o acceso denegado.")
        return obj

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            models.Q(owner=user) | models.Q(collaborators=user)
        ).distinct()

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if not can_edit_project(request.user, project):
            return redirect('projects:project_list')
        return super().dispatch(request, *args, **kwargs)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        # Asegúrate de que collaborators sea iterable de User
        collaborators = form.cleaned_data.get('collaborators', [])
        for user in collaborators:
            if user != self.request.user and user not in self.object.collaborators.all():
                self.object.collaborators.add(user)
        return response


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')

    def test_func(self):
        project = self.get_object()
        return can_edit_project(self.request.user, project)

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_list')

    def test_func(self):
        project = self.get_object()
        return can_delete_project(self.request.user, project)
# --- IGNORE ---