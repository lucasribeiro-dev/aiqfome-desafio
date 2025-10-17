from django.test import TestCase
from clients.models import User
from clients.serializers import ClientSerializer

class ClientSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'username': 'test@example.com',
            'password': 'senha123451@'
        }

    def test_serializer_create_user(self):
        serializer = ClientSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'test@example.com')
        self.assertTrue(user.check_password('senha123451@'))
