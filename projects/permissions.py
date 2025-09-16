from rest_framework import permissions

# --- Funciones base ---
def is_owner(user, project):
    return project.owner == user

def can_edit_project(user, project):
    return user == project.owner or user in project.collaborators.all()

def can_delete_project(user, project):
    return user == project.owner

def can_view_project(user, project):
    return user == project.owner or user in project.collaborators.all()

# --- Clases de permisos ---

class IsProjectOwner(permissions.BasePermission):
    """
    Permite acceso solo al propietario del proyecto.
    """
    def has_object_permission(self, request, view, obj):
        return is_owner(request.user, obj)

class IsProjectOwnerOrCollaborator(permissions.BasePermission):
    """
    Permite acceso si el usuario es owner o colaborador (para cualquier método).
    """
    def has_object_permission(self, request, view, obj):
        return can_view_project(request.user, obj)

class IsProjectOwnerOrCollaboratorReadOnly(permissions.BasePermission):
    """
    Permite lectura a colaboradores y owner, pero escritura solo al owner.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return can_view_project(request.user, obj)
        return is_owner(request.user, obj)

class IsProjectOwnerOrCollaboratorEdit(permissions.BasePermission):
    """
    Permite que tanto el owner como los colaboradores puedan editar.
    """
    def has_object_permission(self, request, view, obj):
        return can_edit_project(request.user, obj)
