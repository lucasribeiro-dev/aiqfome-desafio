from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class ClientViewSetEdgeCasesTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('client-list')

    def test_create_user_with_duplicate_email(self):
        data = {
            'name': 'Teste Duplicado',
            'email': 'duplicado@example.com',
            'password': 'senha123'
        }

        self.client.post(self.list_url, data, format='json')
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_missing_fields(self):
        data = {'name': 'Nome'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_email(self):
        data = {
            'name': 'fake name',
            'email': 'fakeemail',
            'password': 'pass123'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
