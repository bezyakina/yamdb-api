from rest_framework import serializers

from .models import User


class UserEmailSerializer(serializers.Serializer):
    """Сериализатор email пользователя."""

    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор кода подтверждения."""

    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "role",
            "email",
            "first_name",
            "last_name",
            "bio",
        )


class MeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)
