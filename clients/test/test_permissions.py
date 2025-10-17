from django.test import TestCase
from clients.models import User
from clients.permissions import IsAdminOrOwner
from unittest.mock import Mock

class IsAdminOrOwnerPermissionTest(TestCase):
    def setUp(self):
        self.permission = IsAdminOrOwner()
        self.admin_user = User.objects.create_user(
            name='Admin',
            email='admin@example.com',
            username='admin@example.com',
            password='admin123',
            is_staff=True
        )
        self.fulano_user = User.objects.create_user(
            name='Fulano',
            email='fulano@example.com',
            username='fulano@example.com',
            password='fulano123'
        )
        self.joao_user = User.objects.create_user(
            name='Joao',
            email='joao@example.com',
            username='joao@example.com',
            password='joao123'
        )

    def test_admin_has_permission(self):
        request = Mock()
        request.user = self.admin_user

        self.assertTrue(
            self.permission.has_object_permission(request, None, self.joao_user)
        )

    def test_owner_has_permission(self):
        request = Mock()
        request.user = self.fulano_user

        self.assertTrue(
            self.permission.has_object_permission(request, None, self.fulano_user)
        )

    def test_non_owner_no_permission(self):
        request = Mock()
        request.user = self.fulano_user

        self.assertFalse(
            self.permission.has_object_permission(request, None, self.joao_user)
        )
