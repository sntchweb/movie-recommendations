from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.serializers.compilations import (CompilationDetailSerializer,
                                          CompilationListSerializer)
from movies.models.compilations import Compilation


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description='Детальная выдача подборки',
    tags=['Подборки'],
))
class CompilationSoloViewSet(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Compilation.objects.prefetch_related(
        'movies',
        'movies__genres',
        'movies__need_to_see',
        'movies__favorite_for',
    )
    serializer_class = CompilationDetailSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача списка подборок редакции',
    tags=['Подборки'],
))
class CompilationRedactionListViewSet(
    ListModelMixin,
    GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = CompilationListSerializer

    def get_queryset(self):
        new_queryset = Compilation.objects.prefetch_related(
            'movies',
            'movies__genres',
            'movies__need_to_see',
            'movies__favorite_for',
        ).filter(from_redaction=True).order_by('-date_created')
        return new_queryset


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача списка избранных пользователем подборок',
    tags=['Подборки'],
))
class CompilationFavoriteListViewSet(
    ListModelMixin,
    GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompilationListSerializer

    def get_queryset(self):
        user = self.request.user
        new_queryset = user.favorite_compilations.all().order_by(
            '-date_created'
        )
        return new_queryset
