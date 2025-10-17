from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from clients.models import User

class ClientViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('client-list')

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
            password='fulano'
        )
        self.joao_user = User.objects.create_user(
            name='Joao',
            email='joao@example.com',
            username='joao@example.com',
            password='joao123'
        )

    def test_create_user_public(self):
        data = {
            'name': 'Novo Usuario',
            'email': 'newuser@example.com',
            'password': 'usuario123'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(response.data['name'], 'Novo Usuario')
        self.assertEqual(response.data['email'], 'newuser@example.com')
        self.assertNotIn('password', response.data)

    def test_list_users_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 3)

    def test_list_users_fulano_user_forbidden(self):
        self.client.force_authenticate(user=self.fulano_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_own_user(self):
        self.client.force_authenticate(user=self.fulano_user)
        detail_url = reverse('client-detail', kwargs={'pk': self.fulano_user.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'fulano@example.com')

    def test_retrieve_joao_user_forbidden(self):
        self.client.force_authenticate(user=self.fulano_user)
        detail_url = reverse('client-detail', kwargs={'pk': self.joao_user.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_joao_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        detail_url = reverse('client-detail', kwargs={'pk': self.fulano_user.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'fulano@example.com')

    def test_cannot_update_email(self):
        self.client.force_authenticate(user=self.fulano_user)
        detail_url = reverse('client-detail', kwargs={'pk': self.fulano_user.pk})

        patch_data = {'email': 'novoemail@example.com'}
        response_patch = self.client.patch(detail_url, patch_data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

        self.fulano_user.refresh_from_db()
        self.assertEqual(self.fulano_user.email, 'fulano@example.com')

        patch_data = {
            'name': 'Fulano Updated',
            'email': 'mudado@example.com',
            'password': 'fulano'
        }
        response_patch = self.client.patch(detail_url, patch_data, format='json')
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

        self.fulano_user.refresh_from_db()
        self.assertEqual(self.fulano_user.email, 'fulano@example.com')

    def test_delete_own_user(self):
        self.client.force_authenticate(user=self.fulano_user)
        detail_url = reverse('client-detail', kwargs={'pk': self.fulano_user.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)

    def test_delete_joao_user_forbidden(self):
        self.client.force_authenticate(user=self.fulano_user)
        detail_url = reverse('client-detail', kwargs={'pk': self.joao_user.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 3)

    def test_delete_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        detail_url = reverse('client-detail', kwargs={'pk': self.fulano_user.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)

    def test_cannot_set_is_staff_on_creation(self):
        data = {
            'name': 'Admin Test User',
            'email': 'admintestuser@example.com',
            'password': 'senha',
            'is_staff': True
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='admintestuser@example.com')
        self.assertFalse(user.is_staff)
