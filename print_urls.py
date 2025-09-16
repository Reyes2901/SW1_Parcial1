# print_urls.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.urls import get_resolver

urls = get_resolver().url_patterns

for entry in urls:
    print(entry)
