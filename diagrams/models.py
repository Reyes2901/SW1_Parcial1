from django.db import models
from django.conf import settings

class Diagram(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name="diagrams")
    content = models.JSONField(default=dict)
    #created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #si algo falla, cambiar a SET_NULL
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class DiagramVersion(models.Model):
    diagram = models.ForeignKey(Diagram, on_delete=models.CASCADE, related_name="versions")
    content = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    #created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-created_at']
   