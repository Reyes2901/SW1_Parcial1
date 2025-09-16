from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Project, Activity, Comment

@receiver(post_save, sender=Project)
def log_project_save(sender, instance, created, **kwargs):
    action = "creó el proyecto" if created else "editó el proyecto"
    Activity.objects.create(project=instance, user=instance.owner, action=action)

@receiver(post_save, sender=Comment)
def log_comment(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(project=instance.project, user=instance.user, action="comentó en el proyecto")
