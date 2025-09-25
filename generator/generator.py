import os
import zipfile
import shutil
from django.template.loader import render_to_string

def generar_springboot_proyecto(diagrama_json, output_base_dir, app_name="GeneratedApp", package_name="com.example"):
    # Crear carpeta base del proyecto
    project_dir = os.path.join(output_base_dir, "generated_project")
    src_dir = os.path.join(project_dir, "src", "main", "java", *package_name.split('.'))
    resources_dir = os.path.join(project_dir, "src", "main", "resources")

    model_dir = os.path.join(src_dir, "model")
    controller_dir = os.path.join(src_dir, "controller")
    repository_dir = os.path.join(src_dir, "repository")

    # Crear todas las carpetas necesarias
    for path in [model_dir, controller_dir, repository_dir, resources_dir]:
        os.makedirs(path, exist_ok=True)

    clases = diagrama_json.get("classes", [])

    for clase in clases:
        class_name = clase.get("name")
        attributes = clase.get("attributes", [])

        context = {
            "class_name": class_name,
            "attributes": attributes,
            "package_name": package_name
        }

        # Clase modelo
        model_content = render_to_string("java/class.java.j2", context)
        with open(os.path.join(model_dir, f"{class_name}.java"), "w") as f:
            f.write(model_content)

        # Repositorio
        repo_content = render_to_string("java/repository.java.j2", context)
        with open(os.path.join(repository_dir, f"{class_name}Repository.java"), "w") as f:
            f.write(repo_content)

        # Controlador
        ctrl_content = render_to_string("java/controller.java.j2", context)
        with open(os.path.join(controller_dir, f"{class_name}Controller.java"), "w") as f:
            f.write(ctrl_content)

    # Archivo de aplicación principal
    app_context = {
        "app_name": app_name,
        "package_name": package_name,
    }

    main_app_path = os.path.join(src_dir, f"{app_name}Application.java")
    main_app_content = render_to_string("java/Application.java.j2", app_context)
    with open(main_app_path, "w") as f:
        f.write(main_app_content)

    # application.properties
    props_content = render_to_string("java/application.properties.j2", {"app_name": app_name})
    with open(os.path.join(resources_dir, "application.properties"), "w") as f:
        f.write(props_content)

    # pom.xml
    pom_content = render_to_string("java/pom.xml.j2", {"app_name": app_name, "package_name": package_name})
    with open(os.path.join(project_dir, "pom.xml"), "w") as f:
        f.write(pom_content)

    # Crear el .zip
    zip_path = os.path.join(output_base_dir, f"{app_name.lower()}_springboot.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, project_dir)
                zipf.write(filepath, arcname)

    # Limpiar directorio temporal (opcional, solo si quieres limpiar)
    shutil.rmtree(project_dir, ignore_errors=True)

    return zip_path
# Ejemplo de uso:
# diagrama_ejemplo = {  "classes": [{"name": "User", "attributes": [{"name": "id", "type": "Long"}, {"name": "username", "type": "String"}, {"name": "email", "type": "String"}]}, {"name": "Post", "attributes": [{"name": "id", "type": "Long"}, {"name": "title", "type": "String"}, {"name": "content", "type": "String"}, {"name": "userId", "type": "Long"}]}]}            
# generar_springboot_proyecto(diagrama_ejemplo, "/
#ruta/donde/guardar")tmp", app_name="MyApp", package_name="com.mycompany.myapp")
# Asegúrate de tener las plantillas en un directorio llamado "templates/java" dentro de tu app Django.
# Y configura TEMPLATES en settings.py para que incluya 'APP_DIRS': True,
# o agrega la ruta a 'DIRS'.
# Y configura TEMPLATES en settings.py para que incluya 'APP_DIRS': True,