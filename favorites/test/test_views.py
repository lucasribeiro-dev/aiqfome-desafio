from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from clients.models import User
from favorites.models import Favorite


class FavoriteViewSetTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.user = User.objects.create_user(
            username="usertest@example.com",
            email="usertest@example.com",
            password="123456",
            name="User Test"
        )
        self.client_api.force_authenticate(user=self.user)
        self.url_list = reverse("favorite-list")

    @patch("favorites.views.get_product")
    def test_create_favorite_success(self, mock_get_product):
        mock_get_product.return_value = {"title": "Produto Teste", "price": 100.0}
        response = self.client_api.post(self.url_list, {"product_id": 10}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorite.objects.filter(client=self.user, product_id=10).exists())

    @patch("favorites.views.get_product")
    def test_create_favorite_duplicate(self, mock_get_product):
        mock_get_product.return_value = {"title": "Produto Teste"}
        Favorite.objects.create(client=self.user, product_id=1, product_snapshot={"title": "Produto Teste"})

        response = self.client_api.post(self.url_list, {"product_id": 1}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Produto já está nos favoritos.", str(response.data))

    @patch("favorites.views.get_product")
    def test_create_favorite_product_not_found(self, mock_get_product):
        mock_get_product.return_value = None
        response = self.client_api.post(self.url_list, {"product_id": 99}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Produto não encontrado."})

    def test_list_favorites(self):
        Favorite.objects.create(client=self.user, product_id=1, product_snapshot={"title": "Produto 1"})
        response = self.client_api.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["product_id"], 1)
