from rest_framework import serializers

from api.serializers.mixins import (IsFavoriteMixin, IsNeedSeeMixin,
                                    RateInMovieMixin)
from movies.models import Compilation, Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')


class MoviesInCompilationsListSerializer(
    RateInMovieMixin,
    IsFavoriteMixin,
    IsNeedSeeMixin,
    serializers.ModelSerializer
):
    year = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'v_picture',
            'h_picture',
            'year',
            'rating',
            'genres',
            'is_favorite',
            'is_need_see',
        )

    def get_year(self, obj):
        return obj.premiere_date.year


class CompilationDetailSerializer(serializers.ModelSerializer):
    movies = MoviesInCompilationsListSerializer(many=True)

    class Meta:
        model = Compilation
        fields = (
            'id',
            'title',
            'picture',
            'movies',
            'description',
        )


class CompilationListSerializer(serializers.ModelSerializer):
    movies = MoviesInCompilationsListSerializer(many=True)

    class Meta:
        model = Compilation
        fields = ('id', 'title', 'movies', 'description')
