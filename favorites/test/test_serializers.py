from django.test import TestCase
from favorites.serializers import FavoriteSerializer
from favorites.models import Favorite
from clients.models import User

class FavoriteSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="usertest@example.com",
            email="usertest@example.com",
            password="123456",
            name="User Test"
        )

    def test_validate_product_id_success(self):
        serializer = FavoriteSerializer(data={"product_id": 10}, context={"client": self.user})
        self.assertTrue(serializer.is_valid())

    def test_validate_product_id_invalid(self):
        serializer = FavoriteSerializer(data={"product_id": 0}, context={"client": self.user})
        self.assertFalse(serializer.is_valid())
        self.assertIn("product_id deve ser um número positivo", str(serializer.errors))

    def test_duplicate_favorite_validation(self):
        Favorite.objects.create(client=self.user, product_id=5, product_snapshot={})
        serializer = FavoriteSerializer(data={"product_id": 5}, context={"client": self.user})
        self.assertFalse(serializer.is_valid())
        self.assertIn("Produto já está nos favoritos.", str(serializer.errors))
