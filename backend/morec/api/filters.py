from django.db.models import Q
from django_filters import rest_framework as filters

from movies.models import Actor, Director, Movie


class PersonBaseFilter(filters.FilterSet):
    name = filters.CharFilter(method='get_person')

    class Meta:
        fields = ('name',)

    def get_person(self, qs, name, value):
        return qs.filter(
            Q(name__istartswith=value) | Q(last_name__istartswith=value)
        )


class ActorFilter(PersonBaseFilter):
    class Meta(PersonBaseFilter.Meta):
        model = Actor


class DirectorFilter(PersonBaseFilter):
    class Meta(PersonBaseFilter.Meta):
        model = Director


class MoviesFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    orig_title = filters.CharFilter(
        field_name='original_title',
        lookup_expr='icontains',
    )
    actor = filters.NumberFilter(
        field_name='actors',
        lookup_expr='id__exact',
    )
    director = filters.NumberFilter(
        field_name='directors',
        lookup_expr='id__exact',
    )
    genre = filters.CharFilter(
        field_name='genres',
        lookup_expr='slug__exact',
    )
    category = filters.CharFilter(
        field_name='categories',
        lookup_expr='slug__exact',
    )
    country = filters.CharFilter(
        field_name='countries',
        lookup_expr='slug__exact',
    )
    year = filters.NumberFilter(
        field_name='premiere_date',
        lookup_expr='year__exact',
    )
    year_gt = filters.NumberFilter(
        field_name='premiere_date',
        lookup_expr='year__gte',
    )
    year_lt = filters.NumberFilter(
        field_name='premiere_date',
        lookup_expr='year__lte',
    )
    imdb_rate_gt = filters.NumberFilter(
        field_name='rate_imdb',
        lookup_expr='gte',
    )
    imdb_rate_lt = filters.NumberFilter(
        field_name='rate_imdb',
        lookup_expr='lte',
    )

    class Meta:
        model = Movie
        fields = ('title',)
