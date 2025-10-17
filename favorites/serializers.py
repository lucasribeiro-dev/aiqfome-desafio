from rest_framework import serializers
from django.db import IntegrityError
from favorites.models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'client', 'product_id', 'product_snapshot']
        read_only_fields = ['id', 'client', 'product_snapshot']

    def validate_product_id(self, value):
        if value is None:
            raise serializers.ValidationError("product_id é obrigatório.")
        if value <= 0:
            raise serializers.ValidationError("product_id deve ser um número positivo.")
        return value

    def validate(self, attrs):
        client = self.context.get('client')
        product_id = attrs.get('product_id')

        if client and product_id:
            if Favorite.objects.filter(client=client, product_id=product_id).exists():
                raise serializers.ValidationError(
                    {"product_id": "Produto já está nos favoritos."}
                )
        return attrs

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"product_id": "Produto já está nos favoritos."}
            )
