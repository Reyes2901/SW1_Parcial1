FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ Define settings antes de usar cualquier comando Django
ENV DJANGO_SETTINGS_MODULE=backend.settings

RUN python manage.py collectstatic --noinput

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
