from rest_framework import serializers
from .models import User

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "is_staff"]
        read_only_fields = ['id']

        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
        }

    def create(self, validated_data):
        user = User(
            name=validated_data["name"],
            email=validated_data["email"],
            username=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('email', None)

        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
