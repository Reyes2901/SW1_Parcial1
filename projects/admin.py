from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project

admin.site.register(Project)
from .models import Activity, Comment, Diagram
admin.site.register(Activity)
admin.site.register(Comment)    
admin.site.register(Diagram)
# --- IGNORE ---