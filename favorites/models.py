from django.db import models
from django.core.exceptions import ValidationError
from clients.models import User


class Favorite(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product_id = models.PositiveIntegerField()
    product_snapshot = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'product_id')
        indexes = [
            models.Index(fields=['client', 'product_id']),
        ]

    def __str__(self):
        return f'{self.client.name} - {self.product_snapshot.get("title", "Produto")}'

    def clean(self):
        if self.product_id is None:
            raise ValidationError({'product_id': 'Product ID é obrigatório.'})
        if self.product_id <= 0:
            raise ValidationError({'product_id': 'Product ID deve ser um número positivo.'})
