from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from movies.models import Movie


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('rate_imdb', 'rate_kinopoisk')


class RateInMovieMixin(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=RateSerializer)
    def get_rating(self, obj):
        return RateSerializer().to_representation(obj)


class IsFavoriteMixin(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return user in obj.favorite_for.all() if user else False


class IsNeedSeeMixin(serializers.ModelSerializer):
    is_need_see = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_need_see(self, obj):
        user = self.context['request'].user
        return user in obj.need_to_see.all() if user else False
