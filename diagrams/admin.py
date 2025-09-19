from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Diagram

@admin.register(Diagram)
class DiagramAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'created_by', 'created_at')
    search_fields = ('name',)
