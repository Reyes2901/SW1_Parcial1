FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#Establecer la variable de entorno para las settings de Django
ENV DJANGO_SETTINGS_MODULE=backend.settings

RUN python manage.py collectstatic --noinput
# Exponer el puerto que usará Daphne 
#comando por defecto para ejecutar daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
