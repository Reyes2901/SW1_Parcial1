from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    #collaborators = models.ManyToManyField(User, related_name='collaborations', blank=True)
    #Colaborares en proyectos
    collaborators = models.ManyToManyField(User, related_name='collaborated_projects', blank=True)
    
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp} - {self.user.username} - {self.action}'

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:30]}'

class Diagram(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='diagram')
    data = models.JSONField(default=dict)  # Guarda el estado del diagrama como JSON

    def __str__(self):
        return f'Diagram for {self.project.name}'