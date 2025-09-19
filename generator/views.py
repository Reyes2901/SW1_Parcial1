import tempfile
from django.http import FileResponse, Http404
from diagrams.models import Diagram
from .generator import generar_springboot_proyecto

def generar_backend_zip(request, diagram_id):
    try:
        diagram = Diagram.objects.get(id=diagram_id)
    except Diagram.DoesNotExist:
        raise Http404("Diagrama no encontrado")

    content = diagram.content
    temp_dir = tempfile.mkdtemp()
    zip_path = generar_springboot_proyecto(content, temp_dir, app_name="GeneratedApp", package_name="com.example")

    return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename='generated_backend.zip')
