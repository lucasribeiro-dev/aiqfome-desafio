from rest_framework import permissions

class IsAdminOrOwner(permissions.BasePermission):
    """
    Permite acesso total ao admin.
    Usuário comum só pode acessar o próprio perfil.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user
