from rest_framework import viewsets, permissions

from clients.models import User
from clients.serializers import ClientSerializer
from clients.permissions import IsAdminOrOwner
from clients.docs import client_docs

@client_docs
class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action == "list":
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated(), IsAdminOrOwner()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
