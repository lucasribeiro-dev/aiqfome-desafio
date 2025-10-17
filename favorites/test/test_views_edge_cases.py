from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from clients.models import User
from favorites.models import Favorite


class FavoriteEdgeCaseTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.user = User.objects.create_user(
            username="lucas",
            email="lucas@example.com",
            password="123456",
            name="Lucas"
        )
        self.other_user = User.objects.create_user(
            username="maria",
            email="maria@example.com",
            password="123456",
            name="Maria"
        )
        self.api.force_authenticate(user=self.user)
        self.url_list = reverse("favorite-list")

    @patch("favorites.views.get_product")
    def test_create_favorite_missing_product_id(self, mock_get_product):
        mock_get_product.return_value = {"title": "Produto Teste"}
        response = self.api.post(self.url_list, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product_id", response.data)

    @patch("favorites.views.get_product")
    def test_create_favorite_invalid_product_id(self, mock_get_product):
        mock_get_product.return_value = {"title": "Produto Teste"}
        response = self.api.post(self.url_list, {"product_id": 0}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product_id deve ser um número positivo", str(response.data))

    @patch("favorites.views.get_product")
    def test_create_favorite_unauthenticated(self, mock_get_product):
        mock_get_product.return_value = {"title": "Produto Teste"}
        self.api.force_authenticate(user=None)
        response = self.api.post(self.url_list, {"product_id": 10}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Favorite.objects.exists())
