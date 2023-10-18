from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.filters import DirectorFilter
from api.serializers.directors import DirectorSerializer
from movies.models import Director


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача режисёров с фильтрацией',
    tags=['Режисёры'],
))
class DirectorViewSet(ListModelMixin, GenericViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DirectorFilter
