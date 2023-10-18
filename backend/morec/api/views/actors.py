from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.filters import ActorFilter
from api.serializers.actors import ActorSerializer
from movies.models import Actor


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача актёров с фильтрацией',
    tags=['Актёры'],
))
class ActorViewSet(ListModelMixin, GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ActorFilter
