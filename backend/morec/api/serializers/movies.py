from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from api.serializers.mixins import (IsFavoriteMixin, IsNeedSeeMixin,
                                    RateInMovieMixin)
from morec.settings import SHORT_DESCRIPT_LEN, MIN_RATE, MAX_RATE
from movies.models import Category, Country, Genre, Movie, RatingMovie


class GenreInMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')


class CountryInMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'title', 'slug')


class CategoryInMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')


class MoviesListSerializer(
    RateInMovieMixin,
    IsFavoriteMixin,
    IsNeedSeeMixin,
    serializers.ModelSerializer,
):
    year = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)
    countries = CountryInMovieSerializer(many=True)
    actors = serializers.StringRelatedField(many=True)
    directors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'v_picture',
            'h_picture',
            'rating',
            'year',
            'genres',
            'actors',
            'directors',
            'countries',
            'is_favorite',
            'is_need_see',
        )

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_year(self, obj):
        return obj.premiere_date.year


class MoviesFavoritsAndWatchlistSerializer(MoviesListSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'h_picture',
            'rating',
            'year',
            'genres',
            'is_favorite',
            'is_need_see',
        )


class MoviesDetailSerializer(
    RateInMovieMixin,
    IsFavoriteMixin,
    IsNeedSeeMixin,
    serializers.ModelSerializer,
):
    genres = GenreInMovieSerializer(many=True)
    countries = CountryInMovieSerializer(many=True)
    categories = CategoryInMovieSerializer()
    actors = serializers.StringRelatedField(many=True)
    directors = serializers.StringRelatedField(many=True)
    user_rate = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'original_title',
            'v_picture',
            'h_picture',
            'premiere_date',
            'rating',
            'duration_minutes',
            'age_limit',
            'genres',
            'actors',
            'directors',
            'countries',
            'categories',
            'description',
            'is_favorite',
            'is_need_see',
            'trailer_link',
            'user_rate',
        )

    @swagger_serializer_method(serializer_or_field=serializers.FloatField)
    def get_user_rate(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or not obj.ratings.filter(user=user).exists():
            return 0
        return obj.ratings.get(user=user).rate


class MovieRateSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField(
        min_value=MIN_RATE,
        max_value=MAX_RATE,
    )

    class Meta:
        model = RatingMovie
        fields = ('rate',)


class MoviesOfDaySerializer(
    RateInMovieMixin,
    IsFavoriteMixin,
    serializers.ModelSerializer,
):
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'short_description',
            'h_picture',
            'rating',
            'is_favorite',
        )

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_short_description(self, obj):
        pos = obj.description.find(' ', SHORT_DESCRIPT_LEN)
        return obj.description if pos == -1 else obj.description[:pos]
