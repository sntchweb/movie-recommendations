from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers.genres import GenreSerializer
from movies.models import Genre


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача жанров',
    tags=['Жанры'],
))
class GenreViewSet(ListModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
