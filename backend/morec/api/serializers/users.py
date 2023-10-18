import datetime

import jwt
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from morec.settings import JWT_ACCESS_TTL, SECRET_KEY
from users.models import Avatar, User


class UserVerifyEmailSerializer(serializers.ModelSerializer):
    """Сериализатор для проверки почты в db."""

    class Meta:
        model = User
        fields = ('email',)


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = ('email', 'password', 'fav_genres')

    def validate(self, data):
        validate_password(data['password'])
        return data


class LoginSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователей."""

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data['email']
        password = validated_data['password']
        error_msg = 'email или пароль неверны'
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError(error_msg)
            validated_data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        user_id = str(validated_data['user'].id)
        access_payload = {
            'iss': 'backend-api',
            'user_id': user_id,
            'exp': datetime.datetime.now(
                tz=datetime.timezone.utc) + datetime.timedelta(
                seconds=JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(access_payload, SECRET_KEY)

        return {'access': access}


class PasswordRecoverySerializer(serializers.Serializer):
    """Сериализатор для формирования токена для восстановления пароля."""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data['email']
        error_msg = 'email не правильный'
        try:
            user = User.objects.get(email=email)
            if not user:
                raise serializers.ValidationError(error_msg)
            validated_data['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для изменения пароля."""

    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        validate_password(data['new_password'])
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя."""

    class Meta:
        model = User
        fields = ('email', 'username', 'date_of_birth', 'sex', 'fav_genres', 'avatar')
        read_only_fields = ('fav_genres', 'email')


class FavoriteGenresSerializer(serializers.ModelSerializer):
    """Сериализатор для любимых жанров."""

    class Meta:
        model = User
        fields = ('fav_genres',)


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватарок пользователей."""

    class Meta:
        model = Avatar
        fields = ('id', 'avatar')
